__all__ = ["Replace", "replace"]


# standard library
from dataclasses import dataclass, replace as replace_
from enum import auto
from typing import Annotated, Any


# dependencies
from ..core.specs import Specs, TSpec
from ..core.typing import StrPath, TagBase


# constants
class Tag(TagBase):
    ID = auto()
    OF = auto()
    SKIPIF = auto()


@dataclass(frozen=True)
class Replace:
    """Annotation for replacer specs.

    Args:
        id: ID of data spec(s) to be replaced.
        of: Name of data spec attribute to be replaced.
        skipif: Sentinel value for which replacing is skipped.

    """

    id: Annotated[StrPath, Tag.ID]
    """ID of data spec(s) to be replaced."""

    of: Annotated[str, Tag.OF] = "data"
    """Name of data spec attribute to be replaced."""

    skipif: Annotated[Any, Tag.SKIPIF] = None
    """Sentinel value for which replacing is skipped."""


def replace(specs: Specs[TSpec], /) -> Specs[TSpec]:
    """Replace data spec attributes by replacer specs."""
    new = specs.copy()

    for replacer in specs:
        options = specs[replacer.id / "[^/]+"]

        if (
            (id := options[Tag.ID].unique) is None
            or (of := options[Tag.OF].unique) is None
            or (skipif := options[Tag.SKIPIF].unique) is None
        ):
            continue

        if replacer.data == skipif.data:
            continue

        for target in new[id[str].data]:
            changes = {of[str].data: replacer.data}
            updated = replace_(target, **changes)  # type: ignore
            new = new.replace(target, updated)

    return new
