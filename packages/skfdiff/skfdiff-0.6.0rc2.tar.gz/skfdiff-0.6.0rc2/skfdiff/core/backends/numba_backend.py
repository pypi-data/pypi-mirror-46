#!/usr/bin/env python
# coding=utf-8

from operator import attrgetter


import attr
import numba
import numpy
from jinja2 import Template
from loguru import logger
from scipy.sparse import csc_matrix
from sympy import Indexed, KroneckerDelta, Symbol, lambdify, oo
from sympy.printing.lambdarepr import NumPyPrinter
import numpy as np
from cachetools import cachedmethod

from .base_backend import Backend, register_backend
from .numpy_backend import np_Heaviside, np_Max, np_Min


def np_depvar_printer(unk):
    return Symbol(str(unk.discrete))


def np_ivar_printer(coord):
    return (Symbol(str(coord.discrete)), Symbol(str(coord.idx)), coord.step, coord.N)


# @numba.jit(nopython=True, parallel=True, fastmath=True)
@numba.vectorize(
    [numba.float64(numba.float64, numba.float64)], nopython=True, fastmath=True
)
def Min(a, b):
    if a < b:
        return a
    else:
        return b


# @numba.jit(nopython=True, parallel=True, fastmath=True)
@numba.vectorize([numba.float64(numba.float64, numba.float64)], nopython=True)
def Max(a, b):
    if a > b:
        return a
    else:
        return b


@numba.vectorize([numba.float64(numba.float64)], nopython=True)
def Heaviside(x):
    if x < 0:
        return 0
    else:
        return 1


class EnhancedNumPyPrinter(NumPyPrinter):
    def _print_Idx(self, idx, **kwargs):
        return str(idx)

    def _print_Indexed(self, indexed, **kwargs):
        return str(indexed)

    def _print_Min(self, expr):
        return "{0}({1})".format(
            self._module_format("Min"), ",".join(self._print(i) for i in expr.args)
        )

    def _print_Max(self, expr):
        return "{0}({1})".format(
            self._module_format("Max"), ",".join(self._print(i) for i in expr.args)
        )


@register_backend
@attr.s()
class NumbaBackend(Backend):
    name = "numba"
    parallel = attr.ib(default=False, type=bool)
    fastmath = attr.ib(default=True, type=bool)
    nogil = attr.ib(default=True, type=bool)
    printer = EnhancedNumPyPrinter()

    def _convert_inputs(self):
        self.ndim = len(self.system.coordinates)
        self.unks = list(map(np_depvar_printer, self.system.unknowns))
        self.pars = list(map(np_depvar_printer, self.system.parameters))
        self.coords, self.idxs, self.steps, self.sizes = zip(
            *map(np_ivar_printer, self.system.coordinates)
        )
        self.idxs_map = [
            tuple([self.system.coordinates.index(coord) for coord in unk.coordinates])
            for unk in self.system.unknowns
        ]

        self.shapes = [self.system.shapes[unk] for unk in self.system.unknowns]

        self.inputs = [
            self.system._t,
            *self.unks,
            *self.pars,
            *self.coords,
            *self.steps,
            *self.sizes,
        ]
        self.inputs_cond = [*self.idxs, *self.sizes]

    def _build_evolution_equations(self):
        template = Template(
            """
@numba.jit(nopython=True, parallel={{parallel}}, fastmath={{fastmath}}, nogil={{nogil}})
def compute_F_vector({% for item in var_names %}{{ item }}, {% endfor %}grid):
    N = grid.shape[0]
    F = numpy.empty(N)
    for i in numba.prange(N):
        didx, {% for item in var_unpacking %}{{ item }}, {% endfor %}domain, flatidx = grid[i]
        {% for i, expr in exprs %}
        if domain == {{ i }}:
            F[flatidx] = {{ expr }}{% endfor %}
    return F
"""  # noqa
        )
        var_names = self.inputs
        var_unpacking = self.idxs
        self._F_routine_str = template.render(
            var_names=var_names,
            var_unpacking=var_unpacking,
            exprs=enumerate(
                [self.printer.doprint(expr) for expr in self.system.piecewise_system]
            ),
            parallel=self.parallel,
            fastmath=self.fastmath,
            nogil=self.nogil,
        )

        # the routine will be added to the class scope
        exec(self._F_routine_str, globals(), self.__dict__)

    def F(self, fields, t=0):
        unks = [
            fields[varname].values
            for varname in [unk.name for unk in self.system.unknowns]
        ]
        pars = [
            fields[varname].values
            for varname in [par.name for par in self.system.parameters]
        ]
        coords = [
            fields[varname].values
            for varname in [coord.name for coord in self.system.coordinates]
        ]
        sizes = [coord.size for coord in coords]
        grid = self.grid_builder.compute_gridinfo(sizes)
        steps = self.grid_builder.compute_steps(
            tuple(sizes), tuple([coord.ptp() for coord in coords])
        )

        return self.compute_F_vector(t, *unks, *pars, *coords, *steps, *sizes, grid)

    def _build_jacobian(self):

        template = Template(
            """
@numba.jit(nopython=True, parallel={{parallel}}, fastmath={{fastmath}}, nogil={{nogil}})
def compute_jacobian_values({% for item in var_names %}{{ item }},
                            {% endfor %}subgrids, data_size):
    N = len(subgrids)
    data = numpy.zeros(data_size)
    cursor = 0
    jacs_lenght = {{ jacs_len }}

    cursors = [0]
    for i in range(len(subgrids)):
        grid = subgrids[i]
        jl = jacs_lenght[i]
        cursors.append(grid.shape[0] * jl + cursors[-1])
    for i in numba.prange(N):
        cursor = cursors[i]
        grid = subgrids[i]
        M = grid.shape[0]
        {% for jacs in full_jacs %}
        {{ "if" if loop.index==1 else "elif" }} i == {{loop.index0}}: {% if jacs %}{% for jac_func in jacs %}
            next_cursor = cursor + M
            for j in numba.prange(M): {% for item in var_unpacking %}
                {{ item }} = grid[j, {{ loop.index }}]{% endfor %}
                data[cursor + j] = {{ jac_func }}
            cursor = next_cursor {% endfor %}{% else %}
            pass
        {% endif %} {% endfor %}

    return data
        """
        )

        var_names = self.inputs
        var_unpacking = self.idxs
        self._J_routine_str = template.render(
            var_names=var_names,
            var_unpacking=var_unpacking,
            full_jacs=[
                [self.printer.doprint(jac) for jac in jacs]
                for jacs in self.system.jacobian_values
            ],
            jacs_len=[len(jacs) for jacs in self.system.jacobian_values],
            parallel=self.parallel,
            fastmath=self.fastmath,
            nogil=self.nogil,
        )
        logger.debug("generated routine: ")

        # the routine will be added to the class scope
        exec(self._J_routine_str, globals(), self.__dict__)

        # the routine is the same as the numpy backend: they only have to be executed
        # for the first evaluation: no need to rewrite a numba (complex) implementation.

    @cachedmethod(cache=attrgetter("_cache_jac_coord"))
    def compute_jacobian_coordinates(self, *sizes):
        self.jacobian_columns = [
            [lambdify(self.inputs_cond, col) for col in columns]
            for columns in self.system.jacobian_columns
        ]
        subgrids = self.grid_builder.compute_subgrids(sizes)
        system_sizes = self.grid_builder.compute_sizes(sizes)
        system_size = sum(system_sizes)

        rows_list = []
        cols_list = []
        for grid, jac_cols in zip(subgrids, self.jacobian_columns):
            for col_func in jac_cols:
                cols_ = np.zeros((grid.shape[0], self.ndim + 1), dtype="int32")
                cols = col_func(*grid[:, 1:-2].T, *sizes)
                cols = np.stack(
                    [np.broadcast_to(col, cols_.shape[:-1]) for col in cols]
                )

                flat_cols = self.grid_builder.compute_flat_from_idxs(cols.T, sizes)

                rows_list.extend(grid[:, -1].reshape((-1,)))
                cols_list.extend(flat_cols.reshape((-1,)))
        rows = np.array(rows_list)
        cols = np.array(cols_list)

        perm = np.argsort(cols)
        perm_rows = rows[perm]
        perm_cols = cols[perm]
        count = np.zeros((system_size + 1), dtype="int32")
        uq, cnt = np.unique(perm_cols, False, False, True)
        count[uq + 1] = cnt
        indptr = np.cumsum(count)
        return rows, cols, perm_rows, indptr, perm, (system_size, system_size)

    def J(self, fields, t=0):
        unks = [
            fields[varname].values
            for varname in [unk.name for unk in self.system.unknowns]
        ]
        pars = [
            fields[varname].values
            for varname in [par.name for par in self.system.parameters]
        ]
        coords = [
            fields[varname].values
            for varname in [coord.name for coord in self.system.coordinates]
        ]
        sizes = [coord.size for coord in coords]

        steps = self.grid_builder.compute_steps(
            tuple(sizes), tuple([coord.ptp() for coord in coords])
        )
        subgrids = self.grid_builder.compute_subgrids(sizes)
        data_size = sum(
            [
                subgrid.shape[0] * len(jacs)
                for subgrid, jacs in zip(subgrids, self.system.jacobian_columns)
            ]
        )
        data = self.compute_jacobian_values(
            t, *unks, *pars, *coords, *steps, *sizes, subgrids, data_size
        )
        _, _, perm_rows, indptr, perm, shape = self.compute_jacobian_coordinates(*sizes)

        return csc_matrix((data[perm], perm_rows, indptr), shape=shape)

    def __attrs_post_init__(self):
        self._cache_jac_coord = {}
        logger.info("numba backend: convert_inputs...")
        self._convert_inputs()
        logger.info("numba backend: build_evolution_equations...")
        self._build_evolution_equations()
        logger.info("numba backend: build_jacobian...")
        self._build_jacobian()
