#!/usr/bin/env python
# coding=utf-8

from functools import partial, wraps
from itertools import chain
from warnings import warn

import holoviews as hv
from boltons.iterutils import remap
from loguru import logger
from sympy import Dummy, Idx, Indexed, solve
from tqdm import tqdm, tqdm_notebook

tqdm = tqdm


def generate_dummy_map(exprs):
    to_dummify = set(chain(*[expr.atoms(Indexed, Idx) for expr in exprs]))
    dummy_map = {var: Dummy() for var in to_dummify}
    reverse_dummy_map = {dummy: var for var, dummy in dummy_map.items()}
    return dummy_map, reverse_dummy_map


@wraps(solve)
def solve_with_dummy(exprs, vars_, *args, **kwargs):
    def visit_dummy(subs, path, key, value):
        try:
            value = value.subs(subs)
        except AttributeError:
            pass
        try:
            key = key.subs(subs)
        except AttributeError:
            pass
        return key, value

    dummy_map, reverse_dummy_map = generate_dummy_map(exprs)
    dummy_exprs = [expr.subs(dummy_map) for expr in exprs]
    dummy_vars = [var.subs(dummy_map) for var in vars_]
    dummy_sol = solve(dummy_exprs, dummy_vars)
    sol = remap(dummy_sol, visit=partial(visit_dummy, reverse_dummy_map))
    return sol


def _enable_tqdm():
    global tqdm
    try:
        import ipywidgets  # noqa

        tqdm = tqdm_notebook
    except ImportError:
        warn("ipywidgets not installed, skipping tqdm_notebook")


def _enable_bokeh(backends):
    try:
        import bokeh  # noqa

        backends.append("bokeh")
    except ImportError:
        warn("bokeh not installed, skipping this backend")
    return backends


def _enable_matplotlib(backends):
    try:
        import matplotlib  # noqa

        backends.append("matplotlib")
    except ImportError:
        warn("bokeh not installed, skipping this backend")
    return backends


def enable_notebook(enable_tqdm=True, enable_bokeh=True, enable_matplotlib=True):
    if enable_tqdm:
        _enable_tqdm()
    backends = []
    if enable_bokeh:
        backends = _enable_bokeh(backends)
    if enable_matplotlib:
        backends = _enable_matplotlib(backends)

    if backends:
        import logging  # noqa

        hv.notebook_extension(*backends)
        # this function has an annoying side effect and somehow
        # use the root log, add a StreamHandler and put the log
        # level to INFO. This will reset that undesired behaviour.
        root_logging = logging.getLogger()
        root_logging.handlers = []
        root_logging.setLevel("WARNING")


def transform_into_hashable(key):
    try:
        hash(key)
        return key
    except TypeError:
        if isinstance(key, (list, set)):
            return tuple(sorted(key))
        if isinstance(key, dict):
            return tuple(sorted(key.items()))
        return str(key)
