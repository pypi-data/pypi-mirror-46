#!/usr/bin/env python
# coding=utf-8

from functools import partial
from operator import attrgetter

import attr
import numpy as np
from loguru import logger
from scipy.sparse import csc_matrix
from sympy import lambdify, Symbol
from cachetools import cachedmethod

from .base_backend import Backend, register_backend


def np_depvar_printer(unk):
    return Symbol(str(unk.discrete))


def np_ivar_printer(coord):
    return (Symbol(str(coord.discrete)), Symbol(str(coord.idx)), coord.step, coord.N)


def np_Min(args):
    a, b = args
    return np.where(a < b, a, b)


def np_Max(args):
    a, b = args
    return np.where(a < b, b, a)


def np_Heaviside(a):
    return np.where(a < 0, 0, 1)


lambdify = partial(
    lambdify,
    modules=[{"amax": np_Max, "amin": np_Min, "Heaviside": np_Heaviside}, "scipy"],
)


@register_backend
@attr.s
class NumpyBackend(Backend):
    name = "numpy"

    def __attrs_post_init__(self):
        logger.info("numpy backend: convert_inputs...")
        self._convert_inputs()
        logger.info("numpy backend: build_evolution_equations...")
        self._build_evolution_equations()
        logger.info("numpy backend: build_jacobian...")
        self._cache_jac_coord = {}
        self._build_jacobian()

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
            *self.idxs,
            *self.steps,
            *self.sizes,
        ]
        self.inputs_cond = [*self.idxs, *self.sizes]

    def _build_evolution_equations(self):
        self.evolution_equations = [
            lambdify(self.inputs, expr.n()) for expr in self.system.piecewise_system
        ]

    def compute_F_vector(self, t, unks, pars, coords, sizes):
        subgrids = self.grid_builder.compute_subgrids(sizes)
        steps = self.grid_builder.compute_steps(
            tuple(sizes), tuple([coord.ptp() for coord in coords])
        )
        system_sizes = self.grid_builder.compute_sizes(sizes)
        system_size = sum(system_sizes)
        F = np.empty(system_size)
        for grid, eq in zip(subgrids, self.evolution_equations):
            Fi = eq(t, *unks, *pars, *coords, *grid[:, 1:-2].T, *steps, *sizes)
            F[grid[:, -1]] = Fi
        return F

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

        return self.compute_F_vector(t, unks, pars, coords, sizes)

    def _build_jacobian(self):

        self.jacobian_routines = [
            [lambdify(self.inputs, diff) for diff in jac_row]
            for jac_row in self.system.jacobian_values
        ]
        self.jacobian_columns = [
            [lambdify(self.inputs_cond, col) for col in columns]
            for columns in self.system.jacobian_columns
        ]

    def compute_jacobian_values(self, t, unks, pars, coords, sizes):
        subgrids = self.grid_builder.compute_subgrids(sizes)
        steps = self.grid_builder.compute_steps(
            tuple(sizes), tuple([coord.ptp() for coord in coords])
        )
        data_size = sum(
            [
                subgrid.shape[0] * len(jacs)
                for subgrid, jacs in zip(subgrids, self.jacobian_columns)
            ]
        )
        data = np.zeros(data_size)

        cursor = 0
        for grid, jacs in zip(subgrids, self.jacobian_routines):
            for jac_func in jacs:
                next_cursor = cursor + grid.shape[0]
                jac = jac_func(
                    t, *unks, *pars, *coords, *grid[:, 1:-2].T, *steps, *sizes
                )
                data[cursor:next_cursor] = jac
                cursor = next_cursor
        return data

    @cachedmethod(cache=attrgetter("_cache_jac_coord"))
    def compute_jacobian_coordinates(self, *sizes):
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

        data = self.compute_jacobian_values(t, unks, pars, coords, sizes)
        _, _, perm_rows, indptr, perm, shape = self.compute_jacobian_coordinates(*sizes)

        return csc_matrix((data[perm], perm_rows, indptr), shape=shape)
