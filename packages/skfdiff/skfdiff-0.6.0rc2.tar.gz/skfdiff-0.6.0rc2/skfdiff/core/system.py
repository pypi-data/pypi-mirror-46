#!/usr/bin/env python
# coding=utf-8

import re
import typing
from collections import defaultdict
from functools import partial, reduce
from itertools import chain, count, product
from operator import and_, mul
from queue import Queue

import cloudpickle
import attr
from cached_property import cached_property
import numpy as np
from loguru import logger
from more_itertools import unique_everseen
from sympy import (
    Derivative,
    Eq,
    Function,
    Indexed,
    KroneckerDelta,
    Number,
    Symbol,
    Wild,
    Dummy,
    oo,
    solve,
    sympify,
)

from .spatial_schemes import FiniteDifferenceScheme, chain_schemes, upwind
from .variables import Coordinate, Unknown, _convert_coord_list, _convert_unk_list


def _convert_pde_list(pdes):
    if isinstance(pdes, str):
        return [pdes]
    else:
        return pdes


def _partial_derivative(expr, symbolic_coordinates):
    # proxy function that can be easily curried (with functools.partial)
    return Derivative(expr, *symbolic_coordinates)


def _build_sympy_namespace(equation, coordinates, unknowns, parameters):
    """ Check the equation, find all the derivative in Euler notation
    (see https://en.wikipedia.org/wiki/Notation_for_differentiation#Euler's_notation)
    the way that dxxU will be equal to Derivative(U(x), x, x).
    All the derivative found that way are add to a subsitution rule as dict and
    applied when the equation is sympified.
    """

    # look at all the dxxU, dxyV... and dx(...), dxy(...) and so on in the equation
    spatial_derivative_re = re.compile(
        r"d(?P<derargs>\w+?)(?:(?P<depder>(?:%s)+)|\((?P<inder>.*?)\))"
        % "|".join([var.name for var in chain(unknowns, parameters)])
    )
    spatial_derivatives = spatial_derivative_re.findall(str(equation))

    # they can be derivatives inside the dx(...), we check it until there is no more
    queue = Queue()
    [queue.put(sder[2]) for sder in spatial_derivatives if sder[2]]
    while not queue.empty():
        inside_derivative = queue.get()
        new_derivatives = spatial_derivative_re.findall(inside_derivative)
        [queue.put(sder[2]) for sder in new_derivatives if sder[2]]
        spatial_derivatives.extend(new_derivatives)
    # The sympy namespace is built with...
    namespace = dict()
    # All the coordinates
    namespace.update({coord.name: coord.symbol for coord in coordinates})
    # All the dependent variables: unk and parameters
    namespace.update(
        {
            dvar.name: (
                dvar.symbol(*[coord.symbol for coord in dvar.coordinates])
                if dvar.coordinates
                else dvar.symbol
            )
            for dvar in chain(unknowns, parameters)
        }
    )
    # All the harversted derivatives
    for coord, unk, _ in spatial_derivatives:
        if unk:
            namespace["d%s%s" % (coord, unk)] = _partial_derivative(
                namespace[unk], coord
            )
        else:
            namespace["d%s" % coord] = partial(
                _partial_derivative, symbolic_coordinates=coord
            )
    return namespace


def _build_keep_derivs_namespace(equation):
    """ Check the equation, find all the derivative in Euler notation
    (see https://en.wikipedia.org/wiki/Notation_for_differentiation#Euler's_notation)
    the way that dxxU will be equal to Derivative(U(x), x, x).
    All the derivative found that way are add to a subsitution rule as dict and
    applied when the equation is sympified.
    """

    # look at all the dxxU, dxyV... and dx(...), dxy(...) and so on in the equation
    spatial_derivative_re = re.compile(r"D(?P<derargs>\w+?)(?:\((?P<inder>.*)\))")
    spatial_derivatives = spatial_derivative_re.findall(str(equation))

    return spatial_derivatives


def list_node_coords(domain):
    available_node_coords = {}
    for coord, (left_cond, right_cond) in domain.items():
        node_coords = []
        node_coords.append(coord.idx)
        # for both side, left|right_cond can be true : in that case, no coords has to
        # be added : all that side is in the bulk.
        try:
            node_coords.extend(np.arange(coord.idx.lower, left_cond.rhs))
        except AttributeError:
            pass
        try:
            node_coords.extend(
                np.arange(right_cond.rhs - coord.N + 1, coord.idx.upper - coord.N + 1)
                + coord.N
            )
        except AttributeError:
            pass
        available_node_coords[coord] = node_coords
    return available_node_coords


def list_conditions(domain):
    available_conds = {}
    for coord, (left_cond, right_cond) in domain.items():
        conds = []
        conds.append(left_cond & right_cond)
        # for both side, left|right_cond can be true : in that case, no coords has to
        # be added : all that side is in the bulk.
        try:
            conds.extend(
                [
                    Eq(coord.idx, node_coord)
                    for node_coord in np.arange(coord.idx.lower, left_cond.rhs)
                ]
            )
        except AttributeError:
            pass
        try:
            conds.extend(
                [
                    Eq(coord.idx, node_coord)
                    for node_coord in np.arange(
                        right_cond.rhs - coord.N + 1, coord.idx.upper - coord.N + 1
                    )
                    + coord.N
                ]
            )
        except AttributeError:
            pass
        available_conds[coord] = conds
    return available_conds


@attr.s
class PDEquation:
    equation = attr.ib(type=str)
    unknowns = attr.ib(type=typing.Sequence[Unknown], converter=_convert_unk_list)
    parameters = attr.ib(
        type=typing.Sequence[Unknown], converter=_convert_unk_list, default=[]
    )
    subs = attr.ib(type=dict, default={})
    boundary_conditions = attr.ib(type=dict, factory=dict)
    schemes = attr.ib(
        type=typing.Sequence[FiniteDifferenceScheme],
        default=(FiniteDifferenceScheme(),),
        repr=False,
    )
    symbolic_equation = attr.ib(init=False, repr=False)
    fdiff = attr.ib(init=False, repr=False)
    raw = attr.ib(type=bool, default=False, repr=False)
    dirichlet_nodes = attr.ib(
        type=typing.Sequence[typing.Tuple[int, ...]], factory=list, repr=False
    )

    def __attrs_post_init__(self):
        self._t = Symbol("t")
        self._complete_coordinates()
        if self.raw:
            # For "raw" equations already in discretized form as periodic bc
            self.fdiff = sympify(
                self.equation, locals={unk.name: unk.discrete for unk in self.unknowns}
            )
            return
        self._fill_incomplete_unknowns()

        self._sympy_namespace = _build_sympy_namespace(
            self.equation, self.coordinates, self.unknowns, self.parameters
        )
        self._sympify_equation()

        # substitute the auxiliary definition
        sympified_subs = {
            sympify(aux_key, locals=self._sympy_namespace): sympify(
                aux_value, locals=self._sympy_namespace
            )
            for aux_key, aux_value in self.subs.items()
        }
        self.symbolic_equation = self.symbolic_equation.subs(sympified_subs)

        self._as_finite_diff()
        self._reduce_coordinates()

    def __getstate__(self):
        return {key: cloudpickle.dumps(value) for key, value in self.__dict__.items()}

    def __setstate__(self, state):
        self.__dict__.update(
            {key: cloudpickle.loads(value) for key, value in state.items()}
        )

    @property
    def parsed_boundary_conditions(self):
        return dict(self._parse_bc(self.boundary_conditions))

    def _reduce_coordinates(self):
        variables = [
            self.mapper[str(indexed.base)] for indexed in self.fdiff.atoms(Indexed)
        ]
        available_unks = [
            variable for variable in variables if isinstance(variable, Unknown)
        ]
        real_coordinates = set().union(*[unk.coordinates for unk in available_unks])
        self.coordinates = sorted(real_coordinates)

    def _non_expendable_deriv(self, wrts, arg):
        arg = sympify(arg)
        dummy = Function(str(Dummy()))
        dummy_deriv = Derivative(dummy(*self.coordinates), wrts)
        fdiff_dummy = chain_schemes(self.schemes, dummy_deriv)

        def replace_dummy(*coords):
            return arg.subs(
                {
                    symbolic_coord.name: coord
                    for symbolic_coord, coord in zip(self.coordinates, coords)
                }
            )

        return fdiff_dummy.replace(dummy, replace_dummy)

    @property
    def stencils(self):
        stencils = {}
        ref_pde = self([0] * len(self.coordinates))
        indexed = ref_pde.atoms(Indexed)
        for unk in self.unknowns:
            coords = set(
                [
                    tuple(map(int, index.indices))
                    for index in indexed
                    if unk.discrete == index.args[0]
                ]
            )
            ptp = np.array(list(coords)).ptp() + 1
            center = ptp // 2
            stencil_array = np.zeros([ptp] * len(unk.coords), dtype=bool)
            idxs = [np.array(coord + center, dtype=int) for coord in zip(*coords)]
            stencil_array[tuple(idxs)] = True
            stencils[unk.name] = stencil_array
        return stencils

    def _fill_incomplete_unknowns(self):
        """fill every dependent variables that lack information on
        independent variables with the global independent variables
        """
        for i, unk in enumerate(self.unknowns):
            if not unk.coordinates:
                object.__setattr__(self.unknowns[i], "coordinates", self.coordinates)

    def _complete_coordinates(self):
        """if independent variables is not set, extract them from
        the dependent variables. If not set in dependent variables,
        1D resolution with "x" as independent variable is assumed.
        """
        harvested_coords = list(
            chain(
                *[
                    dep_var.coordinates
                    for dep_var in self.unknowns
                    if dep_var.coordinates is not None
                ]
            )
        )
        if harvested_coords:
            self.coordinates = harvested_coords
        else:
            self.coordinates = _convert_coord_list(["x"])
        self.coordinates = list(unique_everseen(self.coordinates))

    def _sympify_equation(self):
        self.symbolic_equation = sympify(self.equation, locals=self._sympy_namespace)
        for unk in self.unknowns:
            self.symbolic_equation = self.symbolic_equation.subs(unk.name, unk.symbol)
        self.symbolic_equation = self.symbolic_equation.doit()

    def _as_finite_diff(self):

        fdiff = self.symbolic_equation
        fdiff = chain_schemes(self.schemes, fdiff)
        fdiff = fdiff.replace(Function("upwind"), upwind)
        to_keep_derivs = _build_keep_derivs_namespace(fdiff)
        for wrts, arg in to_keep_derivs:
            fdiff = fdiff.replace(
                Function("D%s" % "".join(wrts)),
                partial(self._non_expendable_deriv, wrts),
            )

        for coord in self.coordinates:
            a = Wild("a", exclude=[coord.step, coord.symbol, 0])
            fdiff = fdiff.replace(coord.symbol + a * coord.step, coord.idx + a)

        for var in chain(self.unknowns, self.parameters):

            def replacement(*args):
                return var.discrete[args]

            if var.coordinates:
                fdiff = fdiff.replace(var.symbol, replacement)

        for indexed in fdiff.atoms(Indexed):
            new_indexed = indexed.subs(
                {coord.symbol: coord.idx for coord in self.coordinates}
            )
            fdiff = fdiff.subs(indexed, new_indexed)

        fdiff = fdiff.subs(
            {coord.symbol: coord.discrete[coord.idx] for coord in self.coordinates}
        )

        self.fdiff = fdiff

    def __call__(self, coordinates):
        logger.trace("evaluate pde %s at %s" % (self.equation, coordinates))
        subs = {
            coord.idx: coord_value
            for coord, coord_value in zip(self.coordinates, coordinates)
        }
        logger.trace("subs: %s" % subs)
        return self.fdiff.subs(subs)

    def __str__(self):
        return self.__repr__()

    def domains(self, *node_coords):
        return tuple(
            [
                coord.domain(node_coord)
                for coord, node_coord in zip(self.coordinates, node_coords)
            ]
        )

    @property
    def unknowns_dict(self):
        return {unk.name: unk for unk in self.unknowns}

    @property
    def coordinates_dict(self):
        return {
            coord.name: coord
            for coord in set(chain(*[unk.coords for unk in self.unknowns]))
        }

    @property
    def parameters_dict(self):
        return {par.name: par for par in self.parameters}

    @property
    def mapper(self):
        return dict(
            **self.unknowns_dict, **self.parameters_dict, **self.coordinates_dict
        )

    @property
    def physical_domains(self):
        domains = product(*[("left", "bulk", "right") for coord in self.coordinates])
        conds = product(
            *[
                (
                    Eq(coord.idx, coord.idx.lower),
                    (coord.idx.lower < coord.idx) & (coord.idx < coord.idx.upper),
                    Eq(coord.idx, coord.idx.upper),
                )
                for coord in self.coordinates
            ]
        )
        return dict(zip(domains, [reduce(and_, cond) for cond in conds]))

    @property
    def node_coords(self):
        domains = product(*[("left", "bulk", "right") for coord in self.coordinates])

        return [
            tuple(
                coord.get_node_coord(domain)
                for coord, domain in zip(self.coordinates, domain)
            )
            for domain in domains
        ]

    @property
    def node_coords_subs(self):

        return [
            {
                coord.idx: node_coord
                for coord, node_coord in zip(self.coordinates, node_coords)
            }
            for node_coords in self.node_coords
        ]

    def get_domains(self, indexed):
        unk = self.mapper[str(indexed.base)]
        return unk.domains(*indexed.indices)

    def get_distances(self, indexed):
        unk = self.mapper[str(indexed.base)]
        return unk.distances(*indexed.indices)

    def is_in_bulk(self, indexed):
        return not self.is_outside(indexed)

    def is_outside(self, indexed):
        return any(self.get_distances(indexed))

    def _distance_node_to_other(self, node, other_node):
        return tuple(np.abs(np.array(node) - np.array(other_node)))

    def _walk_in_domain(self, node, domains):
        next_node = tuple(node)
        for distance in count():
            local_pde = self(next_node)
            outside_indexed = list(filter(self.is_outside, local_pde.atoms(Indexed)))
            if not outside_indexed:
                break
            next_node = [
                idx + sign_distance(1, domain)
                for idx, domain in zip(next_node, domains)
            ]
        product_distances = product(*[range(distance)] * len(node))
        for distances in product_distances:
            yield tuple(
                [
                    idx + sign_distance(distance, domain)
                    for idx, domain, distance in zip(node, domains, distances)
                ]
            )

    def _parse_bc(self, bcs):
        if isinstance(bcs, str):
            default_bcs = defaultdict(lambda: bcs)
        else:
            default_bcs = defaultdict(lambda: "noflux", bcs)
        unks = [*self.unknowns, *self.parameters]
        for unk, axis in chain(*[product([unk], unk.coords) for unk in unks]):
            yield (unk, axis), BoundaryCondition(
                unk, axis, self, default_bcs[(unk.name, axis.name)]
            )

    # long running, should not be in property
    @cached_property
    def computation_nodes(self):
        extended_computation_nodes = []
        for new_node in chain(
            *[
                self._walk_in_domain(node, domains)
                for node, domains in zip(self.node_coords, self.physical_domains)
            ]
        ):
            extended_computation_nodes.append(new_node)
        return list(set(extended_computation_nodes).union(self.node_coords))

    def _get_filtered_cross(self, coord, node_coords):
        coord_idx = self.coordinates.index(coord)
        cross_node_coords = tuple(
            [node for i, node in enumerate(node_coords) if i != coord_idx]
        )
        cross_computation_nodes = [
            tuple([node for i, node in enumerate(nodes) if i != coord_idx])
            for nodes in self.computation_nodes
        ]
        for i, (computation_node_coords, cross_computation_nodes) in enumerate(
            zip(self.computation_nodes, cross_computation_nodes)
        ):
            ziped_crosses = list(zip(cross_node_coords, cross_computation_nodes))
            same_nodes = [
                node == computation_node for node, computation_node in ziped_crosses
            ]
            bulk_nodes = [
                str(coord.idx) in map(str, computation_node.atoms(Indexed))
                for node, computation_node in ziped_crosses
            ]
            relevant_nodes = [
                (same_node or bulk_node)
                for same_node, bulk_node in zip(same_nodes, bulk_nodes)
            ]
            this_node = computation_node_coords[coord_idx]
            if all(relevant_nodes) and str(coord.idx) not in map(
                str, this_node.atoms()
            ):
                yield this_node

    def _node_to_domain(self, node_coords):
        domain = []
        for i, (coord, node_coord) in enumerate(zip(self.coordinates, node_coords)):
            if str(coord.idx) not in map(str, node_coord.atoms()):
                domain.append(Eq(coord.idx, node_coord))
            else:
                # get all the nodes on the same "cross"
                same_cross_nodes = list(self._get_filtered_cross(coord, node_coords))
                right_nodes = set(
                    [
                        node
                        for node in same_cross_nodes
                        if str(coord.N) in map(str, node.atoms())
                    ]
                )
                left_nodes = set(same_cross_nodes) - right_nodes

                left_node = max(left_nodes)
                right_node = (
                    min([node - coord.idx.upper for node in right_nodes])
                    + coord.idx.upper
                )

                domain.append((left_node < coord.idx) & (coord.idx < right_node))
        return reduce(and_, domain)

    @property
    def computation_domains(self):
        domains = []
        for coord_nodes in self.computation_nodes:
            domains.append(self._node_to_domain(coord_nodes))
        return domains

    def get_ghost_equation(self, ghost, node):
        unk = self.mapper[str(ghost.base)]
        indices = ghost.indices
        domains = self.get_domains(ghost)
        distances = self.get_distances(ghost)
        coords, domains, distances = zip(
            *[
                (coord, domain, distance)
                for coord, domain, distance in zip(unk.coords, domains, distances)
                if distance > 0
            ]
        )
        boundaries = [
            self.parsed_boundary_conditions[unk, coord]
            for coord, domain in zip(coords, domains)
        ]
        eqs, kinds = zip(
            *[
                (
                    bc.get(
                        domain,
                        domains={
                            coord: domain
                            for coord, domain in zip(
                                unk.coords, self.get_domains(ghost)
                            )
                        },
                        evaluation_node=ghost,
                        offset=-distance,
                    ),
                    getattr(bc, "kind_%s" % domain),
                )
                for bc, coord, domain, distance in zip(
                    boundaries, coords, domains, distances
                )
            ]
        )
        for eq, kind, domain, coord in zip(eqs, kinds, domains, coords):
            if kind != "periodic":
                eval_indices = [
                    index
                    if coord_idx != coord
                    else (coord.idx.lower if domain == "left" else coord.idx.upper)
                    for index, coord_idx in zip(indices, unk.coordinates)
                ]
                return eq(eval_indices)
            else:
                return eq(indices)

    def _extrapolate_coords(self, local_eq):
        outside_coords = [
            idx
            for idx in filter(self.is_outside, local_eq.atoms(Indexed))
            if isinstance(self.mapper[str(idx.base)], Coordinate)
        ]
        for indexed_coord in outside_coords:
            coord = self.mapper[str(indexed_coord.base)]
            index = indexed_coord.indices[0]
            distance = coord.distance_from_domain(index)
            domain = coord.domain(index)
            if domain == "left":
                rhs = coord.discrete[coord.idx.lower] - coord.step * distance
            else:
                rhs = coord.discrete[coord.idx.upper] + coord.step * distance
            logger.debug(
                "extrapolate outside coordinate, subs: {%s: %s}" % (indexed_coord, rhs)
            )
            local_eq = local_eq.subs(indexed_coord, rhs)
        return local_eq

    def _get_ghosts(self, local_eq):
        return [
            idx
            for idx in filter(self.is_outside, local_eq.atoms(Indexed))
            if isinstance(self.mapper[str(idx.base)], Unknown)
        ]

    # long running, should not be in property
    @cached_property
    def piecewise_system(self):
        piecewise_system = []
        for node_coord, domain in zip(self.computation_nodes, self.computation_domains):
            if node_coord in self.dirichlet_nodes:
                piecewise_system.append(Number(0))
                continue
            local_eq = self._extrapolate_coords(self(node_coord))
            ghosts = self._get_ghosts(local_eq)
            while ghosts:
                logger.debug("ghosts: %s" % ghosts)
                eqs = [self.get_ghost_equation(ghost, node_coord) for ghost in ghosts]
                solved = solve(eqs, ghosts, dict=True)
                local_eq = self._extrapolate_coords(local_eq.subs(solved[0]))
                ghosts = self._get_ghosts(local_eq)
            piecewise_system.append(local_eq)
        return tuple(piecewise_system)


def sign_distance(distance, domain):
    if domain == "bulk":
        return 0
    if domain == "left":
        return distance
    return -distance


def dict_product(d):
    keys = d.keys()
    for element in product(*d.values()):
        yield dict(zip(keys, element))


@attr.s
class PDESys:
    evolution_equations = attr.ib(
        type=typing.Sequence[str], converter=_convert_pde_list
    )
    unknowns = attr.ib(type=typing.Sequence[Unknown], converter=_convert_unk_list)
    parameters = attr.ib(
        type=typing.Sequence[Unknown], converter=_convert_unk_list, factory=list
    )
    coordinates = attr.ib(
        type=typing.Sequence[Coordinate],
        default=[],
        converter=_convert_coord_list,
        repr=False,
    )
    boundary_conditions = attr.ib(type=dict, factory=dict)
    subs = attr.ib(type=dict, factory=dict)
    # domains = attr.ib(type=dict, default=None, init=False, repr=False)

    def _coerce_equations(self):
        self.evolution_equations = [
            PDEquation(
                eq,
                self.unknowns,
                self.parameters,
                subs=self.subs,
                boundary_conditions=self.boundary_conditions,
            )
            for eq in self.evolution_equations.copy()
        ]
        self._apply_dirichlet()
        self.coordinates = sorted(
            set(chain(*[eq.coordinates for eq in self.evolution_equations.copy()]))
        )

    def _apply_dirichlet(self):
        for unk, pde in zip(self.unknowns, self.evolution_equations):
            for domains, coord_node in zip(pde.physical_domains, pde.node_coords):
                bcs = [
                    pde.parsed_boundary_conditions[(unk, coord)]
                    for coord in unk.coordinates
                ]
                kinds = [
                    getattr(bc, "kind_%s" % domain)
                    for bc, domain in zip(bcs, domains)
                    if domain != "bulk"
                ]
                if "Dirichlet" in kinds:
                    pde.dirichlet_nodes.append(coord_node)

    def _get_shapes(self):
        self.pivot = None

        gridinfo = dict(zip(self.coordinates, [coord.N for coord in self.coordinates]))

        shapes = []
        for unk in self.unknowns:
            gridshape = [
                (gridinfo[coord] if coord in unk.coordinates else 1)
                for coord in self.coordinates
            ]
            shapes.append(tuple(gridshape))
        sizes = [reduce(mul, shape) for shape in shapes]
        self.size = sum(sizes)

        self.shapes = dict(zip(self.unknowns, shapes))
        self.sizes = dict(zip(self.unknowns, sizes))

    def __attrs_post_init__(self):
        logger.info("processing pde system")
        logger.info("coerce equations...")
        self._t = Symbol("t")
        self._coerce_equations()
        self._get_shapes()
        logger.info("done")

    def _sort_indexed(self, indexed):
        unk_idx = [unk.name for unk in self.unknowns].index(str(indexed.args[0]))
        coords = self.unknowns[unk_idx].coordinates
        idxs = indexed.args[1:]
        idxs = [
            idxs[coords.index(coord)] if coord in coords else 0
            for coord in self.coordinates
        ]
        return [unk_idx, *idxs]

    def _filter_unk_indexed(self, indexed):
        return indexed.base in [unk.discrete for unk in self.unknowns]

    def _simplify_kron(self, *kron_args):
        kron = KroneckerDelta(*kron_args)
        return kron.subs({coord.N: oo for coord in self.coordinates})

    @cached_property
    def piecewise_system(self):
        return list(chain(*(pde.piecewise_system for pde in self)))

    @cached_property
    def jacobian_values(self):
        jacobian_values = []
        for expr in self.piecewise_system:
            wrts = list(filter(self._filter_unk_indexed, expr.atoms(Indexed)))
            diffs = [
                expr.diff(wrt).replace(KroneckerDelta, self._simplify_kron).n()
                for wrt in wrts
            ]
            jacobian_values.append(diffs)
        return jacobian_values

    @cached_property
    def jacobian_columns(self):
        jacobian_columns = []
        for expr in self.piecewise_system:
            wrts = list(filter(self._filter_unk_indexed, expr.atoms(Indexed)))
            grids = list(map(self._sort_indexed, wrts))
            jacobian_columns.append(grids)
        return jacobian_columns

    @property
    def unknowns_dict(self):
        return {unk.name: unk for unk in self.unknowns}

    @property
    def coordinates_dict(self):
        return {
            coord.name: coord
            for coord in set(chain(*[unk.coords for unk in self.unknowns]))
        }

    @property
    def parameters_dict(self):
        return {par.name: par for par in self.parameters}

    @property
    def mapper(self):
        return dict(
            **self.unknowns_dict, **self.parameters_dict, **self.coordinates_dict
        )

    @property
    def equation_dict(self):
        return {
            unk.name: equation
            for unk, equation in zip(self.unknowns, self.evolution_equations)
        }

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.evolution_equations[key]
        if isinstance(key, str):
            return self.equation_dict[key]
        raise KeyError(key)


def target_axis(derivative, wrt, axis):
    return wrt == axis.symbol


@attr.s
class BoundaryCondition:
    unknown = attr.ib(type=Unknown, converter=Unknown)
    axis = attr.ib(type=Coordinate, converter=Coordinate)
    pde = attr.ib(PDEquation)
    bcs = attr.ib(type=typing.Optional[typing.Union[str, typing.Tuple[str, str]]])
    left = attr.ib(type=PDEquation, init=False, repr=False)
    right = attr.ib(type=PDEquation, init=False, repr=False)
    kind_left = attr.ib(type=str, init=False)
    kind_right = attr.ib(type=typing.Union[typing.Tuple[str, str], str], init=False)

    @bcs.default
    def noflux_default(self):
        return ("noflux", "noflux")

    @bcs.validator
    def bcs_validator(self, attribute, value):
        if value in ["periodic", "noflux"]:
            return True
        if not isinstance(value, str) and len(value) == 2:
            return True

    def _build_bcs(self, bcs):
        if bcs == "periodic":
            left = self._build_periodic("left")
            right = self._build_periodic("right")
            return (left, "periodic"), (right, "periodic")
        if bcs == "noflux":
            bcs = ("noflux", "noflux")
        return (self._build_bc(bc) for bc in bcs)

    def _build_bc(self, eq):
        kind = None
        if eq is None or eq == "noflux":
            eq = "d%s%s" % (self.axis.name, self.unknown.name)
        if eq == "dirichlet":
            eq = "d%s%s" % (self.axis.name, self.unknown.name)
            kind = "Dirichlet"

        return eq, kind or "Ghost"

    def _build_periodic(self, side):
        unk = self.unknown
        axis = self.axis
        if side == "left":
            substitute = axis.idx + axis.N
        else:
            substitute = axis.idx - axis.N
        return unk.discrete_i - unk.discrete_i.subs(axis.idx, substitute)

    def __attrs_post_init__(self):
        self.bcs = self.bcs or "noflux"
        (self.left, self.kind_left), (self.right, self.kind_right) = self._build_bcs(
            self.bcs
        )

    def evaluate_side_patterns(self, node, coord, domain):
        if coord == self.axis:
            return
        if str(node) == str(coord.idx):
            return
        if domain == "bulk" and str(coord.idx) in map(str, node.atoms(Symbol)):
            this_offset = node - coord.idx
            if this_offset > 0:
                scheme = "left"
            else:
                scheme = "right"
        elif domain == "bulk":
            return
        else:
            if domain == "right":
                scheme = "left"
            else:
                scheme = "right"
        return FiniteDifferenceScheme(
            scheme=scheme, pattern=partial(target_axis, axis=coord)
        )

    def get(self, side, domains, evaluation_node, offset=None):
        if getattr(self, "kind_%s" % side) == "periodic":
            return PDEquation(self._build_periodic(side), self.unknown, raw=True)
        if offset is None:
            offset = 1

        if side == "left":
            scheme = "right"
            main_offset = offset
        else:
            scheme = "left"
            main_offset = -offset

        main_scheme = FiniteDifferenceScheme(
            scheme=scheme,
            offset=main_offset,
            pattern=partial(target_axis, axis=self.axis),
        )

        schemes = [main_scheme]

        for node, (coord, domain) in zip(evaluation_node.indices, domains.items()):
            scheme = self.evaluate_side_patterns(node, coord, domain)
            if scheme:
                schemes.append(scheme)

        return PDEquation(
            getattr(self, side),
            self.pde.unknowns,
            self.pde.parameters,
            schemes=schemes[::-1],
        )
