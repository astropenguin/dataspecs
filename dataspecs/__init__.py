__all__ = [
    "core",
    "ROOT",
    "Path",
    "Spec",
    "Specs",
    "StrPath",
    "TagBase",
    "from_dataclass",
    "from_typehint",
]
__version__ = "5.0.0"


# dependencies
from . import core
from .core.api import *
from .core.specs import *
from .core.typing import *
