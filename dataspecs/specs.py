__all__ = ["Spec", "Specs"]


# standard library
from dataclasses import dataclass, field, fields
from typing import Any


# dependencies
from .typing import (
    DataClass,
    TagBase,
    get_annotated,
    get_dataclasses,
    get_subscriptions,
    get_tags,
)


# constants
ROOT = "root"


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

    @classmethod
    def from_dataclass(cls, dc: DataClass) -> "Specs":
        """Create data specifications from a dataclass object."""
        return from_dataclass(dc)


def from_dataclass(dc: DataClass, root: str = ROOT) -> Specs:
    """Create data specifications from a dataclass object."""
    specs = Specs()

    for f in fields(dc):
        spec = Spec(
            id=(id_ := f"{root}.{f.name}"),
            type=(annotated := get_annotated(f.type)),
            data=getattr(dc, f.name, f.default),
            tags=list(get_tags(f.type)),
            origin=dc,
        )

        specs.append(spec)
        specs.extend(from_typehint(annotated, id_))

        for dc_ in get_dataclasses(f.type):
            specs.extend(from_dataclass(dc_, id_))

    return specs


def from_typehint(hint: Any, root: str = ROOT) -> Specs:
    """Create data specifications from a type hint."""
    specs = Specs()

    for name, type_ in enumerate(get_subscriptions(hint)):
        spec = Spec(
            id=(id_ := f"{root}.{name}"),
            type=Any,
            data=(annotated := get_annotated(type_)),
            tags=list(get_tags(type_)),
            origin=hint,
        )

        specs.append(spec)
        specs.extend(from_typehint(annotated, id_))

        for dc_ in get_dataclasses(type_):
            specs.extend(from_dataclass(dc_, id_))

    return specs
