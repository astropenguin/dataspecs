__all__ = ["Attr", "ID", "Name", "Spec", "Tag", "Tags", "Type", "Unit", "Value"]


# standard library
from collections.abc import Hashable
from dataclasses import dataclass
from typing import Any, Generic, Literal, Optional, TypeVar


# dependencies
from typing_extensions import TypeGuard


# type hints
TAny = TypeVar("TAny")
AttrName = Literal["id", "name", "tags", "type", "unit", "value"]


@dataclass(frozen=True)
class Spec(Generic[TAny]):
    """Data specification (data spec)."""

    id: str
    """Data-spec ID."""

    name: Hashable
    """Data-spec name."""

    tags: set[str]
    """Data-spec tags."""

    type: type[Any]
    """Type of the data-spec value."""

    unit: Optional[str]
    """Unit of the data-spec value."""

    value: Optional[TAny]
    """Data-spec value or its default."""


class Attr(Generic[TAny]):
    """Wrapper for data-spec attributes."""

    def __init__(self, wrapped: TAny, /) -> None:
        self.wrapped = wrapped

    def __repr__(self) -> str:
        """Return string of <class name>(<wrapped value>)."""
        return f"{type(self).__name__}({self.wrapped!r})"


class ID(Attr[str]):
    """Wrapper for a data-spec ID."""

    pass


class Name(Attr[Hashable]):
    """Wrapper for a data-spec name."""

    pass


class Tag(Attr[str]):
    """Wrapper for a data-spec tag."""

    pass


class Tags(Attr[set[str]]):
    """Wrapper for data-spec tags."""

    pass


class Type(Attr[type[Any]]):
    """Wrapper for a data-spec type."""

    pass


class Unit(Attr[str]):
    """Wrapper for a data-spec unit."""

    pass


class Value(Attr[str]):
    """Wrapper for a data-spec value."""

    pass


def is_id(obj: Any, /) -> TypeGuard[ID]:
    """Check if given object is a wrapped data-spec ID."""
    return isinstance(obj, ID)


def is_name(obj: Any, /) -> TypeGuard[Name]:
    """Check if given object is a wrapped data-spec name."""
    return isinstance(obj, Name)


def is_tag(obj: Any, /) -> TypeGuard[Tag]:
    """Check if given object is a wrapped data-spec tag."""
    return isinstance(obj, Tag)


def is_tags(obj: Any, /) -> TypeGuard[Tags]:
    """Check if given object is wrapped data-spec tags."""
    return isinstance(obj, Tags)


def is_type(obj: Any, /) -> TypeGuard[Type]:
    """Check if given object is a wrapped data-spec type."""
    return isinstance(obj, Type)


def is_unit(obj: Any, /) -> TypeGuard[Unit]:
    """Check if given object is a wrapped data-spec unit."""
    return isinstance(obj, Unit)


def is_value(obj: Any, /) -> TypeGuard[Value]:
    """Check if given object is a wrapped data-spec value."""
    return isinstance(obj, Value)
