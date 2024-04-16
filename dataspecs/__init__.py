__all__ = [
    # subpackages
    "core",
    "extras",
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
from . import extras


# aliases
from .core.api import *
from .core.specs import *
from .core.typing import *
