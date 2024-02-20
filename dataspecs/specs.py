__all__ = ["Spec", "Specs"]


# standard library
from dataclasses import dataclass, field
from typing import Any


# dependencies
from .typing import TagBase


@dataclass
class Spec:
    """Data specification.

    Args:
        id: Identifier of the specification.
        type: Type (hint) of the specification.
        data: Data of the specification.
        tags: Tags of the specification.
        origin: Origin of the specification.

    """

    id: str
    """Identifier of the specification."""

    type: Any
    """Type (hint) of the specification."""

    data: Any
    """Data of the specification."""

    tags: list[TagBase] = field(default_factory=list)
    """Tags of the specification."""

    origin: Any = field(default=None, repr=False)
    """Origin of the specification."""


class Specs(list[Spec]):
    """Data specifications."""

    pass

