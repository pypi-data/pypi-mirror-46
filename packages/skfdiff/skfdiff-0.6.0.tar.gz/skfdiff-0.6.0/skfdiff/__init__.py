#!/usr/bin/env python
# coding=utf-8
# flake8: noqa

from loguru import logger

from .utils import enable_notebook  # noqa
from .core import temporal_schemes as schemes  # noqa
from .core.temporal_schemes import Stationnary as StationnarySolver
from .model import Model  # noqa
from .simulation import Simulation  # noqa
from .core.system import PDESys, PDEquation  # noqa
from .core.grid_builder import GridBuilder  # noqa
from .core import backends

from .plugins.container import Container  # noqa
from .plugins.displays import Display  # noqa

retrieve_container = Container.retrieve
display_fields = Display.display_fields

from ._version import get_versions  # noqa

__version__ = get_versions()["version"]
del get_versions

import sys

logger.disable(__name__)
