__all__ = [
    "ID",
    "ROOT",
    "Data",
    "Name",
    "Spec",
    "Specs",
    "Tag",
    "Type",
    "api",
    "from_dataclass",
    "from_typehint",
    "specs",
    "typing",
]
__version__ = "5.0.0"


# dependencies
from . import api
from . import specs
from . import typing
from .api import *
from .specs import *
from .typing import *
