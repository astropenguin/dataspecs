__all__ = ["Format", "format"]


# standard library
from dataclasses import dataclass, replace
from enum import auto
from typing import Annotated, Any, cast


# dependencies
from ..core.specs import Specs, TSpec
from ..core.typing import StrPath, TagBase


# constants
class Tag(TagBase):
    ID = auto()
    OF = auto()
    SKIPIF = auto()


@dataclass(frozen=True)
class Format:
    """Annotation for formatter specs."""

    id: Annotated[StrPath, Tag.ID]
    """ID of data spec(s) to be formatted."""

    of: Annotated[str, Tag.OF] = "data"
    """Name of data spec attribute to be formatted."""

    skipif: Annotated[Any, Tag.SKIPIF] = None
    """Sentinel value for which formatting is skipped."""


def format(specs: Specs[TSpec], /) -> Specs[TSpec]:
    """Format data spec attributes by formatter specs."""
    new = specs.copy()

    for formatter in specs:
        options = specs[formatter.id / "*"]

        if (
            (id := options[Tag.ID].unique) is None
            or (of := options[Tag.OF].unique) is None
            or (skipif := options[Tag.SKIPIF].unique) is None
        ):
            continue

        if formatter.data == skipif.data:
            continue

        for target in new[id.data]:
            attr: str = getattr(target, (name := cast(str, of.data)))
            changes = {name: attr.format(formatter.data)}
            updated = replace(target, **changes)  # type: ignore
            new = new.replace(target, updated)

    return new
