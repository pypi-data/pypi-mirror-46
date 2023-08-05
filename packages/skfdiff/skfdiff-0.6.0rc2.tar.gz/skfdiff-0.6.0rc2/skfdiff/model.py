#!/usr/bin/env python
# coding=utf-8

import sys
import warnings
from copy import deepcopy
from itertools import chain

import forge
import numpy as np
import cloudpickle

# from loguru import logger
from xarray import Dataset

from .core.backends import get_backend
from .core.grid_builder import GridBuilder
from .core.system import PDESys
from .simulation import Simulation, null_hook


sys.setrecursionlimit(40000)
EPS = 1e-6


def create_fields(coords, unks, pars):
    unk_names = [unk.name for unk in unks]
    ivar_names = [coord.name for coord in coords]
    par_names = [par.name for par in pars]

    @forge.sign(
        *[forge.kwarg(name=name) for name in chain(ivar_names, unk_names, par_names)]
    )
    def Fields(**kwargs):
        """Create a xarray Dataset as expected by the model input."""
        return Dataset(
            data_vars={
                unk.name: (
                    unk.c_names,
                    np.broadcast_to(
                        kwargs[unk.name], (kwargs[coord].size for coord in unk.c_names)
                    ).copy(),
                )
                for unk in chain(unks, pars)
            },
            coords={coord.name: kwargs[coord.name] for coord in coords},
        )

    return Fields


class Model:
    r"""Contain finite difference approximation and routine of the dynamical system.

    Take a mathematical form as input, use Sympy to transform it as a symbolic
    expression, perform the finite difference approximation and expose theano
    optimized routine for both the right hand side of the dynamical system and
    Jacobian matrix approximation.

    Parameters
    ----------
    evolution_equations : Union[Sequence[str], str]
        the right hand sides of the partial differential equations written
        as :math:`\\frac{\\partial U}{\\partial t} = F(U)`, where the spatial
        derivative can be written as `dxxU` or `dx(U, 2)` or with the sympy
        notation `Derivative(U, x, x)`
    unknowns : Union[Sequence[str], str]
        the dependent variables with the same order as the temporal
        derivative of the previous arg.
    parameters : Optional[Union[Sequence[str], str]]
        list of the parameters. Can be feed with a scalar of an array with
        the same size. They can be derivated in space as well.
    boundary_conditions : Optional[Union[str, Dict[str, Dict[str, Tuple[str, str]]]]]
        Can be either "noflux" (default behavior), "periodic", or a dictionary that
        follow this structure :
        {dependent_var: {indep_var: (left_boundary, right_boundary)}}, the boundaries
        being written as residual (rhs - lhs = 0).
        For example, an hybrid Dirichlet / Neumann flux will be written as
        {"U": {"x": (dxU - 2, U - 3)}}. If a boundary is None, a nul flux will be
        applied.
    subs : Optional[Dict[str, str]]
        Substitution dictionnary, useful to write complex systems. The key of this
        dictionnary will be substitued everywhere in the evolution equations as well
        as in boundary conditions.
    backend: str, default to "numpy"
        A registered backend that will take the discretized system and expose the evolution
        equations routine ``F`` as well as an optional Jacobian routine ``J``. If the later is
        not provided by the backend, the implicit methods will not be available.
        TODO: make an efficient jacobian approximation for that case, given the bandwidth.
        For now, there is the ``numpy`` backend, that provide efficient (but not optimal)
        computation with minimal dependencies, and ``numba`` backend that provide a LLVM based
        routine that allow faster parallel computation at the costs of a (sometime long) warm-up.
        The numba one is less tested and stable, but provide a potential huge speed-up for explicit
        methods.
    backend_kwargs: Optional[Dict] : supplementary arguments provided to the backend.

    Examples
    --------
    A simple diffusion equation:

    >>> from skfdiff import Model
    >>> model = Model("k * dxxU", "U", "k")

    A coupled system of convection-diffusion equation:

    >>> from skfdiff import Model
    >>> model = Model(["k1 * dxxU - c1 * dxV",
    ...                "k2 * dxxV - c2 * dxU",],
    ...                ["U", "V"], ["k1", "k2", "c1", "c2"])

    A 2D pure advection model, without / with upwind scheme.

    >>> from skfdiff import Model
    >>> model = Model("c_x * dxU + c_y * dyU", "U(x, y)",
    ...               ["c_x", "c_y"])
    >>> model = Model("upwind(c_x, U, x, 2) + upwind(c_y, U, y, 2)",
    ...               "U(x, y)",
    ...               ["c_x", "c_y"])


    A 2D diffusion model, with hybrid boundary conditions (Dirichlet, Neuman, Robin and No-flux).

    >>> from skfdiff import Model
    >>> model = Model("dxxU + dyyU", "U(x, y)",
    ...               boundary_conditions={("U", "x"): ("U - 3", "dxU + 5"),
    ...                                    ("U", "y"): ("dyU - (U - 3)", None)
    ...                                   })

    """  # noqa

    def __init__(
        self,
        evolution_equations,
        unknowns,
        parameters=None,
        coordinates=None,
        boundary_conditions=None,
        subs=None,
        backend="numpy",
        backend_kwargs=None,
    ):
        if parameters is None:
            parameters = []
        if coordinates is None:
            coordinates = []
        if boundary_conditions is None:
            boundary_conditions = {}
        if subs is None:
            subs = {}
        if backend_kwargs is None:
            backend_kwargs = {}

        self.evolution_equations = evolution_equations
        self.unknowns = deepcopy(unknowns)
        self.parameters = deepcopy(parameters)
        self.coordinates = deepcopy(coordinates)
        self.boundary_conditions = deepcopy(boundary_conditions)
        self.subs = deepcopy(subs)

        self.pdesys = PDESys(
            evolution_equations=self.evolution_equations,
            unknowns=self.unknowns,
            coordinates=self.coordinates,
            parameters=self.parameters,
            boundary_conditions=self.boundary_conditions,
            subs=self.subs,
        )

        self.grid_builder = GridBuilder(self.pdesys)

        self.backend = get_backend(backend)(
            self.pdesys, self.grid_builder, **backend_kwargs
        )

    @property
    def Fields(self):
        """Base for structured fields stored in a xarray."""
        return create_fields(
            self.pdesys.coordinates, self.pdesys.unknowns, self.pdesys.parameters
        )

    def F(self, fields, t=0):
        """Compute the right hand side of the dynamical system"""
        return self.backend.F(fields, t=t)

    def J(self, fields, t=0):
        """Compute the Jacobian of the dynamical system as sparce csc matrix"""
        try:
            return self.backend.J(fields, t=t)
        except AttributeError:
            raise AttributeError(
                "current backend %s lack of routine to compute the jacobian matrix. "
                "Only explicite scheme will be working." % self.backend.name
            )

    def U_from_fields(self, fields, t=0):
        """Get a fields and return the data as a single flat vector."""
        return self.grid_builder.U_from_fields(fields, t=t)

    def fields_from_U(self, U, fields, t=0):
        """take a solution ad single flat vector and return structured fields."""
        return self.grid_builder.fields_from_U(U, fields, t=t)

    def __getstate__(self):
        return {key: cloudpickle.dumps(value) for key, value in self.__dict__.items()}

    def __setstate__(self, state):
        self.__dict__.update(
            {key: cloudpickle.loads(value) for key, value in state.items()}
        )

    def __repr__(self):
        if not self.boundary_conditions:
            bdc = "noflux"
        elif isinstance(self.boundary_conditions, dict):
            bdc = "\n".join(self.boundary_conditions.items())
        else:
            bdc = self.boundary_conditions
        return """System
-------
{pdesys}

Boundary condition
------------------
{bdc}

backend
-------
{backend}
""".format(
            pdesys="\n\n".join(
                [
                    "dt%s = %s" % (unk, pde.equation)
                    for unk, pde in zip(self.unknowns, self.pdesys)
                ]
            ),
            bdc=bdc,
            backend=self.backend.name,
        )

    def fields_template(self, *args, **kwargs):
        warnings.warn(
            "This interface is deprecied, use model.Fields instead. Will be removed in the 0.7.0",
            DeprecationWarning,
        )
        return self.Fields(*args, **kwargs)

    def init_simulation(
        self,
        fields,
        dt,
        t=0,
        tmax=None,
        id=None,
        hook=null_hook,
        scheme="RODASPR",
        time_stepping=True,
        **kwargs
    ):
        """Init a skfdiff Simulation. See skfdiff.simulation.Simulation docstring
        for further details.
        """
        return Simulation(
            model=self,
            fields=fields,
            dt=dt,
            t=t,
            tmax=tmax,
            id=id,
            hook=hook,
            scheme=scheme,
            time_stepping=time_stepping,
            **kwargs
        )
