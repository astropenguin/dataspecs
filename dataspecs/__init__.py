__all__ = [
    # subpackages
    "core",
    "extras",
    # aliases (core)
    "ROOT",
    "Path",
    "Spec",
    "Specs",
    "StrPath",
    "TagBase",
    "from_dataclass",
    "from_typehint",
    # aliases (extras)
    "Format",
    "FormatTag",
    "Name",
    "NameTag",
    "Replace",
    "ReplaceTag",
    "format",
    "name",
    "replace",
]
__version__ = "5.0.0"


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
