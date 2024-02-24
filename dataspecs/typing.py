__all__ = ["DataClass", "TagBase"]


# standard library
from dataclasses import Field, is_dataclass
from enum import Enum
from os import PathLike, fspath
from pathlib import PurePosixPath
from typing import Annotated, Any, ClassVar, Protocol, Union


# dependencies
from typing_extensions import TypeGuard, get_args, get_origin


# type hints
StrPath = Union[str, PathLike[str]]


class DataClass(Protocol):
    """Type hint for any dataclass object."""

    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]


class ID(PurePosixPath):
    """Identifier (ID) for data specifications."""

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


class TagBase(Enum):
    """Tag base for data specifications."""

    pass


def get_annotated(hint: Any) -> Any:
    """Return annotated type of a type hint if it exists."""
    return get_args(hint)[0] if is_annotated(hint) else hint


def get_annotations(hint: Any) -> tuple[Any, ...]:
    """Return annotations of a type hint if they exist."""
    return get_args(hint)[1:] if is_annotated(hint) else ()


def get_dataclasses(hint: Any) -> tuple[DataClass, ...]:
    """Return dataclass objects that annotate a type hint."""
    return tuple(filter(is_dataclass, get_annotations(hint)))


def get_subscriptions(hint: Any) -> tuple[Any, ...]:
    """Return subscriptions of a type hint if they exist."""
    return get_args(get_annotated(hint))


def get_tags(hint: Any) -> tuple[TagBase, ...]:
    """Return tags that annotate a type hint."""
    return tuple(filter(is_tag, get_annotations(hint)))


def is_annotated(hint: Any) -> bool:
    """Check if a type hint is annotated."""
    return get_origin(hint) is Annotated


def is_tag(obj: Any) -> TypeGuard[TagBase]:
    """Check if an object is a specification tag."""
    return isinstance(obj, TagBase)
