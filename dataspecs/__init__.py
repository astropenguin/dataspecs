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
    "Name",
    "Replace",
    "format",
    "name",
    "replace",
]
__version__ = "3.0.1"


# subpackages
from . import core
from . import extras


# aliases (core)
from .core.api import *
from .core.specs import *
from .core.typing import *


# aliases (extras)
from .extras.formatting import *
from .extras.naming import *
from .extras.replacing import *
