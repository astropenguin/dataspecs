__all__ = ["Spec", "Specs"]


# standard library
from dataclasses import dataclass, field, fields
from typing import Any


# dependencies
from typing_extensions import Self
from .typing import (
    ID,
    DataClass,
    TagBase,
    get_annotated,
    get_dataclasses,
    get_subscriptions,
    get_tags,
)


# constants
ROOT = ID("/")


@dataclass
class Spec:
    """Data specification.

    Args:
        id: Identifier of the specification.
        type: Type hint of the specification.
        data: Data of the specification.
        tags: Tags of the specification.
        origin: Origin of the specification.

    """

    id: ID
    """Identifier of the specification."""

    type: Any
    """Type hint of the specification."""

    data: Any
    """Data of the specification."""

    tags: list[TagBase] = field(default_factory=list)
    """Tags of the specification."""

    origin: Any = field(default=None, repr=False)
    """Origin of the specification."""


class Specs(list[Spec]):
    """Data specifications."""

    @classmethod
    def from_dataclass(cls, dc: DataClass, parent: ID = ROOT) -> Self:
        """Create data specifications from a dataclass object.

        Args:
            dc: Dataclass object to be parsed.
            parent: Identifier of the parent.

        Returns:
            Data specifications created from ``dc``.

        """
        specs = cls()

        for f in fields(dc):
            spec = Spec(
                id=(id_ := parent / f.name),
                type=(annotated := get_annotated(f.type)),
                data=getattr(dc, f.name, f.default),
                tags=list(get_tags(f.type)),
                origin=dc,
            )

            specs.append(spec)
            specs.extend(cls.from_typehint(annotated, id_))

            for dc_ in get_dataclasses(f.type):
                specs.extend(cls.from_dataclass(dc_, id_))

        return specs

    @classmethod
    def from_typehint(cls, hint: Any, parent: ID = ROOT) -> Self:
        """Create data specifications from a type hint.

        Args:
            hint: Type hint to be parsed.
            parent: Identifier of the parent.

        Returns:
            Data specifications created from ``hint``.

        """
        specs = cls()

        for name, type_ in enumerate(get_subscriptions(hint)):
            spec = Spec(
                id=(id_ := parent / str(name)),
                type=Any,
                data=(annotated := get_annotated(type_)),
                tags=list(get_tags(type_)),
                origin=hint,
            )

            specs.append(spec)
            specs.extend(cls.from_typehint(annotated, id_))

            for dc_ in get_dataclasses(type_):
                specs.extend(cls.from_dataclass(dc_, id_))

        return specs

    def children(self, parent: Spec) -> Self:
        """Select specifications that are children of the parent."""
        cls = type(self)
        return cls([spec for spec in self if is_child(spec, parent)])

def is_child(spec: Spec, parent: Spec) -> bool:
    """Check if a specification is a child of the parent."""
    return (spec.id != parent.id) and spec.id.is_relative_to(parent.id)
