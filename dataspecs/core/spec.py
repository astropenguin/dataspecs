__all__ = ["Attr", "ID", "Name", "Spec", "Tag", "Type", "Unit", "Value"]


# standard library
from collections.abc import Hashable
from dataclasses import dataclass
from typing import Any, Callable, Generic, Literal, Optional, TypeVar


# dependencies
from typing_extensions import TypeGuard


# type hints
TAny = TypeVar("TAny")
TSpec = TypeVar("TSpec", bound="Spec[Any]")
SpecAttr = Literal["id", "name", "tags", "type", "unit", "value"]
SpecFactory = Callable[..., TSpec]


@dataclass(frozen=True)
class Spec(Generic[TAny]):
    """Data specification (data spec)."""

    id: str
    """Data spec ID."""

    name: Hashable
    """Data spec name."""

    tags: list[str]
    """Data spec tags."""

    type: type[Any]
    """Type of the data spec value."""

    unit: Optional[str]
    """Unit of the data spec value."""

    value: Optional[TAny]
    """Data spec value or its default."""


class Attr(Generic[TAny]):
    """Wrapper for data spec attributes."""

    def __init__(self, wrapped: TAny, /) -> None:
        self.wrapped = wrapped

    def __repr__(self) -> str:
        """Return string of <class name>(<wrapped value>)."""
        return f"{type(self).__name__}({self.wrapped!r})"


class ID(Attr[str]):
    """Wrapper for data spec IDs."""

    pass


class Name(Attr[Hashable]):
    """Wrapper for data spec names."""

    pass


class Tag(Attr[str]):
    """Wrapper for data spec tags."""

    pass


class Type(Attr[type[Any]]):
    """Wrapper for data spec types."""

    pass


class Unit(Attr[str]):
    """Wrapper for data spec units."""

    pass


class Value(Attr[str]):
    """Wrapper for data spec values."""

    pass


def is_id(obj: Any, /) -> TypeGuard[ID]:
    """Check if given object is a wrapped ID."""
    return isinstance(obj, ID)


def is_name(obj: Any, /) -> TypeGuard[Name]:
    """Check if given object is a wrapped name."""
    return isinstance(obj, Name)


def is_tag(obj: Any, /) -> TypeGuard[Tag]:
    """Check if given object is a wrapped tag."""
    return isinstance(obj, Tag)


def is_type(obj: Any, /) -> TypeGuard[Type]:
    """Check if given object is a wrapped type."""
    return isinstance(obj, Type)


def is_unit(obj: Any, /) -> TypeGuard[Unit]:
    """Check if given object is a wrapped unit."""
    return isinstance(obj, Unit)


def is_value(obj: Any, /) -> TypeGuard[Value]:
    """Check if given object is a wrapped value."""
    return isinstance(obj, Value)
