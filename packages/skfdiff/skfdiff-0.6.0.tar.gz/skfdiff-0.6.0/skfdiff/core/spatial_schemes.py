#!/usr/bin/env python
# coding=utf-8

from itertools import chain, product
from typing import Dict, Sequence

import attr
from sympy import Derivative, Max, Min

from .variables import Coordinate


def as_finite_diff(derivative, coord, offset=0, accuracy=2, scheme="centered"):
    try:
        order = dict(derivative.variable_count)[coord.symbol]
    except KeyError:
        return derivative
    if scheme == "centered":
        n = (order + 1) // 2 + accuracy - 2
        stencil = tuple(range(-n + offset, n + 1 + offset))
    elif scheme == "right":
        n = accuracy + order
        stencil = tuple(range(0 + offset, n + offset))

    elif scheme == "left":
        n = accuracy + order
        stencil = tuple(range(-(n - 1) + offset, 1 + offset))

    else:
        raise NotImplementedError(
            "scheme should be one of 'centered', 'left' or 'right'."
        )
    points = [coord.symbol + i * coord.step for i in stencil]
    return derivative.as_finite_difference(points=points, wrt=coord.symbol), stencil


def all_derivatives(derivative, wrt):
    return True


@attr.s()
class FiniteDifferenceScheme:
    scheme = attr.ib(type=str, default="centered")
    accuracy = attr.ib(type=int, default=2)
    offset = attr.ib(type=int, default=0)
    pattern = attr.ib(default=all_derivatives, repr=False)

    def relevant_derivatives(self, expr):
        derivatives = expr.atoms(Derivative)
        return list(
            [
                (deriv, coord)
                for deriv, coord in chain(
                    *[
                        product([derivative], derivative.variables)
                        for derivative in derivatives
                    ]
                )
                if self.pattern(deriv, coord)
            ]
        )

    def pop_derivative(self, expr):
        derivative, coord = list(self.relevant_derivatives(expr))[0]
        coord = Coordinate(str(coord))
        return derivative, coord

    def apply(self, expr):
        while self.relevant_derivatives(expr):
            derivative, coord = self.pop_derivative(expr)
            discrete_derivative, stencil = as_finite_diff(
                derivative,
                coord,
                accuracy=self.accuracy,
                offset=self.offset,
                scheme=self.scheme,
            )
            expr = expr.replace(derivative, discrete_derivative)
        return expr


def upwind(velocity, unk, coord=None, accuracy=2):
    if coord is None and len(unk.args) == 1:
        coord = unk.args[0]
    elif coord is None:
        raise ValueError(
            "You have to provide the coordinate where the upwind scheme apply for non 1D unknown."
        )

    def left_deriv(coord, unk):
        deriv = Derivative(unk, (coord, 1))
        n = accuracy + 1
        if accuracy < 3:
            stencil = tuple(range(-(n - 1), 1))

        elif accuracy == 3:
            stencil = tuple(range(-(n - 2), 2))
        else:
            raise NotImplementedError("Upwind is only available for n <= 3")
        points = [coord.symbol + i * coord.step for i in stencil]
        discretized_deriv = deriv.as_finite_difference(points=points, wrt=coord.symbol)
        return discretized_deriv

    def right_deriv(coord, unk):
        deriv = Derivative(unk, (coord, 1))
        n = accuracy + 1
        if accuracy < 3:
            stencil = tuple(range(0, n))
        elif accuracy == 3:
            stencil = tuple(range(-1, n - 1))
        else:
            raise NotImplementedError("Upwind is only available for n <= 3")
        points = [coord.symbol + i * coord.step for i in stencil]
        discretized_deriv = deriv.as_finite_difference(points=points, wrt=coord.symbol)
        return discretized_deriv

    ap = Max(velocity, 0)
    am = Min(velocity, 0)

    coord = Coordinate(str(coord))

    deriv_left = left_deriv(coord, unk)
    deriv_right = right_deriv(coord, unk)
    discretized_deriv = ap * deriv_left + am * deriv_right
    return discretized_deriv


def chain_schemes(schemes, expr, default_scheme="centered", default_accuracy=2):
    for scheme in [*schemes, FiniteDifferenceScheme(default_scheme, default_accuracy)]:
        expr = scheme.apply(expr)
    return expr
