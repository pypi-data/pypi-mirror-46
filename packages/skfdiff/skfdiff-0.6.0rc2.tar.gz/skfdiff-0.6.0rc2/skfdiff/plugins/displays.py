#!/usr/bin/env python
# coding=utf-8

from collections import defaultdict
from functools import partial

from holoviews import Curve, DynamicMap, Image, Layout, streams
from loguru import logger
from path import Path  # noqa


class Display:
    def __init__(self, skel_data, plot_function):

        self._plot_pipe = streams.Pipe(data=skel_data)
        self._dynmap = DynamicMap(plot_function, streams=[self._plot_pipe])

    def _repr_mimebundle_(self, *args, **kwargs):
        return self.hv_curve._repr_mimebundle_(*args, **kwargs)

    def connect(self, stream, n=1):
        stream.partition(n).pluck(-1).sink(self._plot_pipe.send)

    @property
    def hv_curve(self):
        return self._dynmap.collate()

    def show(self):
        return self.hv_curve

    def __add__(self, other):
        if isinstance(other, Display):
            return self._dynmap + other._dynmap
        return self._dynmap + other

    def __mul__(self, other):
        if isinstance(other, Display):
            return self._dynmap * other._dynmap
        self._dynmap * other

    @staticmethod
    def display_custom(simul, plot_function, n=1):
        def wrapped_plot_function(data):
            return plot_function(data)

        display = Display(simul, wrapped_plot_function)
        display.connect(simul.stream, n)
        return display

    @staticmethod
    def display_fields(simul, keys="unknowns", n=1, dim_allowed=(0, 1, 2)):
        _0D_history = defaultdict(
            list
        )  # mypy: Dict[str, Sequence[Tuple[float, float]]]

        def plot_function(keys, _0D_history, data):
            curves = []
            if keys == "all":
                keys = data.fields.data_vars
            elif keys == "unknowns":
                parameters = [par.name for par in simul.model.pdesys.parameters]
                keys = [
                    key
                    for key in data.fields.data_vars
                    if key in set(data.fields.data_vars).difference(parameters)
                ]
            if not keys:
                raise ValueError("keys are empty.")
            for var in keys:
                displayed_field = data.fields[var]
                if 0 in dim_allowed and len(displayed_field.dims) == 0:
                    _0D_history[var].append((simul.t, float(data.fields[var])))
                    curve = Curve(_0D_history[var], kdims="t", vdims=var, label=var)
                    curves.append(curve)

                if 1 in dim_allowed and len(displayed_field.dims) == 1:
                    curves.append(Curve((displayed_field.squeeze()), label=var))
                elif 2 in dim_allowed and len(displayed_field.dims) == 2:
                    curves.append(Image((displayed_field.squeeze()), label=var))
                else:
                    continue
            return Layout(curves)

        display = Display(simul, partial(plot_function, keys, _0D_history))
        display.connect(simul.stream, n)
        display.cols = display.hv_curve.cols
        return display
