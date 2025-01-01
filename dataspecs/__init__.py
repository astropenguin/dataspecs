__all__ = [
    # subpackages
    "core",
    "extras",
    # aliases (core)
    "ID",
    "ROOT",
    "Spec",
    "Specs",
    "TagBase",
    "from_dataclass",
    "from_typehint",
    # aliases (extras)
    "Format",
    "Replace",
    "format",
    "replace",
]
__version__ = "2.0.1"


# subpackages
from . import core
from . import extras


# aliases (core)
from .core.api import *
from .core.specs import *
from .core.typing import *


# aliases (extras)
from .extras.formatting import *
from .extras.replacing import *
