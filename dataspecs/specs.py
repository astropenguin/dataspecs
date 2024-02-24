__all__ = ["Spec", "Specs"]


# standard library
from dataclasses import dataclass, field, fields
from os import PathLike, fspath
from pathlib import PurePosixPath
from typing import Any, Union


# dependencies
from typing_extensions import Self
from .typing import (
    DataClass,
    TagBase,
    get_annotated,
    get_dataclasses,
    get_subscriptions,
    get_tags,
)


# type hints
StrPath = Union[str, PathLike[str]]


# constants
ROOT = ID("/")


class ID(PurePosixPath):
    """Identifier (ID)."""

    def __init__(self, *segments: StrPath) -> None:
        """Create an ID from path segments."""
        super().__init__(*segments)

        if not self.root:
            raise ValueError("ID must start with the root.")

    def is_child(self, other: StrPath) -> bool:
        """Check if the ID is a child of other ID."""
        return self.match(f"{other}/*")

    def is_parent(self, other: StrPath) -> bool:
        """Check if the ID is the parent of other ID."""
        return type(self)(other).match(f"{self}/*")

    def matches(self, pattern: StrPath) -> bool:
        """Check if the ID matches a pattern."""
        return self.match(fspath(pattern))


@dataclass
class Spec:
    """Data specification.

    Args:
        id: Identifier of the specification.
        tags: Tags of the specification.
        type: Type hint of the specification.
        data: Data of the specification.
        origin: Origin of the specification.

    """

    id: ID
    """Identifier of the specification."""

    tags: list[TagBase]
    """Tags of the specification."""

    type: Any = field(repr=False)
    """Type hint of the specification."""

    data: Any = field(repr=False)
    """Data of the specification."""

    origin: Any = field(repr=False)
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
