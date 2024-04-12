__all__ = [
    # subpackages
    "core",
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


# subpackages
from . import core


# aliases
from .core.api import *
from .core.specs import *
from .core.typing import *
