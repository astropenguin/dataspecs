__all__ = [
    # subpackages
    "core",
    # aliases (core)
    "ID",
    "Name",
    "Spec",
    "Specs",
    "Tag",
    "Tags",
    "Type",
    "Unit",
    "Value",
    "from_dataclass",
    "from_typehint",
]
__version__ = "5.0.0"


# subpackages
from . import core


# aliases (core)
from .core.api import *
from .core.spec import *
from .core.specs import *
