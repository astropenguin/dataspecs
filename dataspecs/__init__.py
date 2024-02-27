__all__ = [
    # submodules
    "api",
    "specs",
    "typing",
    # aliases
    "ID",
    "ROOT",
    "Spec",
    "Specs",
    "TagBase",
]
__version__ = "0.0.2"


# submodules
from . import api
from . import specs
from . import typing


# aliases
from .specs import *
from .typing import *
