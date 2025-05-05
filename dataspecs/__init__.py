__all__ = [
    "core",
    "Attr",
    "Data",
    "ID",
    "Name",
    "Spec",
    "Specs",
    "Tag",
    "Type",
    "Unit",
    "from_dataclass",
    "from_typehint",
]
__version__ = "5.0.0"


# dependencies
from . import core
from .core.api import *
from .core.spec import *
from .core.specs import *
