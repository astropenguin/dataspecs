__all__ = ["Spec", "Specs"]


# standard library
from dataclasses import dataclass, field, fields
from typing import Any, Union


# dependencies
from typing_extensions import Self
from .typing import (
    DataClass,
    ID,
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
    """Data specification (data spec).

    Args:
        id: ID of the data spec.
        tags: Tags of the data spec.
        type: Type hint of the data spec.
        data: Data of the data spec.
        origin: Origin of the data spec.

    """

    id: ID
    """ID of the data spec."""

    tags: list[TagBase]
    """Tags of the data spec."""

    type: Any = field(repr=False)
    """Type hint of the data spec."""

    data: Any = field(repr=False)
    """Data of the data spec."""

    origin: Any = field(repr=False)
    """Origin of the data spec."""

    def is_child(self, other: Self) -> bool:
        """Check if the data spec is a child of other one."""
        return self.id.is_child(other.id)

    def is_parent(self, other: Self) -> bool:
        """Check if the data spec is the parent of other one."""
        return self.id.is_parent(other.id)

    def matches(self, pattern: StrPath) -> bool:
        """Check if the data spec matches a pattern."""
        return self.id.matches(pattern)


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

    def members(self, group: TagBase) -> Self:
        """Select specifications that are members of the tag group."""
        cls = type(self)
        return cls([spec for spec in self if is_member(spec, group)])


def is_child(spec: Spec, parent: Spec) -> bool:
    """Check if a specification is a child of the parent."""
    return (spec.id != parent.id) and spec.id.is_relative_to(parent.id)


def is_member(spec: Spec, group: TagBase) -> bool:
    """Check if a specification is a member of the tag group."""
    return any(tag is group for tag in spec.tags)
