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
    "from_dataclass",
    "from_typehint",
]
__version__ = "0.2.0"


# submodules
from . import api
from . import specs
from . import typing


# aliases
from .api import *
from .specs import *
from .typing import *
