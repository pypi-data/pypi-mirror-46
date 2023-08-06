# -*- coding: utf-8 -*-

"""Top-level package for mason."""

__author__ = """Eric Hulser"""
__email__ = 'eric.hulser@gmail.com'

try:
    from ._version import __version__
except ImportError:
    __version__ = '0.0.0'

from . import nodes  # noqa: F401, F403
from .blueprint import Blueprint  # noqa: F401
from .group import Group  # noqa: F401
from .node import Node  # noqa: F401

from .library import (  # noqa: F401
    Library,
    get_library,
    set_library,
    library_context,
)
