#!/usr/bin/env python
# coding=utf-8

import re
import string
import typing
from functools import reduce
from itertools import product
from operator import and_

import attr
from sympy import Eq, Function, Idx, IndexedBase, Symbol


@attr.s(frozen=True, repr=False, hash=False)
class Coordinate:
    name = attr.ib(type=str, converter=str)

    @name.validator
    def check(self, attrs, value):
        if not isinstance(value, Coordinate) and (
            value not in string.ascii_letters or len(value) > 1
        ):
            raise ValueError(
                "independant variables have to be 1 char "
                "lenght and be an ascii letter "
                '(is "%s")' % value
            )

    @property
    def coords(self):
        return (self,)

    @property
    def c_symbols(self):
        return tuple([coord.symbol for coord in self.coords])

    @property
    def c_names(self):
        return tuple([coord.name for coord in self.coords])

    @property
    def c_steps(self):
        return tuple([coord.step for coord in self.coords])

    @property
    def c_step_values(self):
        return tuple([coord.step_value for coord in self.coords])

    @property
    def c_discs(self):
        return tuple([coord.discrete for coord in self.coords])

    @property
    def c_idxs(self):
        return tuple([coord.idx for coord in self.coords])

    @property
    def c_Ns(self):
        return tuple([coord.N for coord in self.coords])

    @property
    def c_bounds(self):
        return tuple([coord.bound for coord in self.coords])

    @property
    def symbol(self):
        return Symbol(self.name)

    @property
    def discrete(self):
        return IndexedBase(self.name)

    @property
    def N(self):
        return Symbol("N_%s" % self.name, integer=True)

    @property
    def bound(self):
        return (0, self.N - 1)

    def get_node_coord(self, domain):
        if domain == "left":
            return self.idx.lower
        if domain == "right":
            return self.idx.upper
        return self.idx

    def domains(self, *node_coords):
        return tuple(
            [
                coord.domain(node_coord)
                for coord, node_coord in zip(self.coords, node_coords)
            ]
        )

    def domain(self, node_coord):
        def to_bool(cond):
            try:
                cond = cond.subs(self.N, 500)
            except AttributeError:
                pass
            return cond

        is_left = to_bool(node_coord <= self.idx.lower)
        is_right = to_bool(node_coord >= self.idx.upper)
        # if x_idx is in the node_coord, it belong to the bulk.
        # Otherwise, it's only if it's neither into the left and the right.
        try:
            if str(self.idx) in map(str, node_coord.atoms()):
                return "bulk"
        except AttributeError:
            pass
        if not is_left and not is_right:
            return "bulk"
        if is_left:
            return "left"
        if is_right:
            return "right"

    def is_in_bulk(self, node_coord):
        return True if self.domain(node_coord) == "bulk" else False

    def distance_from_domain(self, node_coord):
        if self.domain(node_coord) == "bulk":
            return 0
        if self.domain(node_coord) == "left":
            return int(self.idx.lower - node_coord)
        if self.domain(node_coord) == "right":
            return int(node_coord - self.idx.upper)

    def distances(self, node_coord):
        return (self.distance_from_domain(node_coord),)

    @property
    def idx(self):
        return Idx("%s_idx" % self.name, self.N)

    @property
    def step(self):
        return Symbol("d%s" % self.name)

    @property
    def step_value(self):
        return (self.discrete[self.idx.upper] - self.discrete[self.idx.lower]) / (
            self.N - 1
        )

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash(self.name)


_dependent_var_re = re.compile(r"^(?P<unk>\w+)(?:\((?P<unkarg>[^\)]*)\))?$")


@attr.s(frozen=True, repr=False, hash=False)
class Unknown:
    name = attr.ib(type=str)
    coordinates = attr.ib(init=False, type=typing.Tuple[Coordinate])

    def __attrs_post_init__(self):
        if isinstance(self.name, Unknown):
            name, coordinates = self.name.name, self.name.coords
        else:
            name, coordinates = Unknown._convert(self.name)
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "coordinates", coordinates)

    @staticmethod
    def _convert(var):
        match = _dependent_var_re.match(var)
        if not match:
            raise ValueError("Dependent variable not properly formatted.")

        unk, coords = _dependent_var_re.findall(var)[0]
        return (
            unk,
            tuple(
                [
                    Coordinate(coord.strip())
                    for coord in coords.split(",")
                    if coord != ""
                ]
            ),
        )

    @property
    def coords(self):
        return self.coordinates

    @property
    def c_symbols(self):
        return tuple([coord.symbol for coord in self.coords])

    @property
    def c_names(self):
        return tuple([coord.name for coord in self.coords])

    @property
    def c_steps(self):
        return tuple([coord.step for coord in self.coords])

    @property
    def c_step_values(self):
        return tuple([coord.step_value for coord in self.coords])

    @property
    def c_discs(self):
        return tuple([coord.discrete for coord in self.coords])

    @property
    def c_idxs(self):
        return tuple([coord.idx for coord in self.coords])

    @property
    def c_Ns(self):
        return tuple([coord.N for coord in self.coords])

    @property
    def c_bounds(self):
        return tuple([coord.bound for coord in self.coords])

    def domains(self, *node_coords):
        return tuple(
            [
                coord.domain(node_coord)
                for coord, node_coord in zip(self.coords, node_coords)
            ]
        )

    def distances(self, *node_coords):
        return [
            coord.distance_from_domain(node_coord)
            for coord, node_coord in zip(self.coords, node_coords)
        ]

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

    def is_in_bulk(self, *node_coords):
        return tuple(
            [
                coord.is_in_bulk(node_coord)
                for coord, node_coord in zip(self.coords, node_coords)
            ]
        )

    @property
    def symbol(self):
        return Function(self.name) if self.coords else Symbol(self.name)

    @property
    def discrete(self):
        return IndexedBase(self.name) if self.coords else Symbol(self.name)

    def __len__(self):
        return len(self.coords)

    @property
    def discrete_i(self):
        return self.discrete[self.c_idxs] if self.coords else Symbol(self.name)

    def __repr__(self):
        return "{}{}".format(
            self.name,
            ("(%s)" % ", ".join(map(str, self.coords)) if self.coords else ""),
        )

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash(self.__str__())


def _convert_unk_list(unknowns):
    def convert_unknown(unk):
        if isinstance(unk, str):
            return Unknown(unk)
        if isinstance(unk, Unknown):
            return unk
        raise ValueError("dependent var should be string or Unknown")

    if not isinstance(unknowns, (list, tuple)):
        return [convert_unknown(unknowns)]
    else:
        return tuple(list(map(convert_unknown, unknowns)))


def _convert_coord_list(coordinates):
    def convert_coord(coordinate):
        if isinstance(coordinate, str):
            return Coordinate(coordinate)
        if isinstance(coordinate, Coordinate):
            return coordinate
        raise ValueError("dependent var should be string or Coordinate")

    if not isinstance(coordinates, (list, tuple)):
        return [convert_coord(coordinates)]
    else:
        return tuple(list(map(convert_coord, coordinates)))
