__all__ = ["Attr", "ID", "Name", "Spec", "Tag", "Type", "Unit", "Value"]


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

    tags: frozenset[str]
    """Data-spec tags."""

    type: Any
    """Type of the data-spec value."""

    unit: Optional[str]
    """Unit of the data-spec value."""

    value: Optional[TAny]
    """Data-spec value or its default."""

    @property
    def id_(self) -> "ID":
        """Wrapped data-spec ID."""
        return ID(self.id)

    @property
    def name_(self) -> "Name":
        """Wrapped data-spec name."""
        return Name(self.name)

    @property
    def tags_(self) -> set["Tag"]:
        """Wrapped data-spec tags."""
        return set(Tag(tag) for tag in self.tags)

    @property
    def type_(self) -> "Type":
        """Wrapped type of the data-spec value."""
        return Type(self.type)

    @property
    def unit_(self) -> "Unit":
        """Wrapped unit of the data-spec value."""
        return Unit(self.unit)

    @property
    def value_(self) -> "Value":
        """Wrapped data-spec value or its default."""
        return Value(self.value)


class Attr(Generic[TAny]):
    """Wrapper for data-spec attributes."""

    def __init__(self, attr: TAny, /) -> None:
        self.attr = attr

    def __repr__(self) -> str:
        """Return string of <class name>(<wrapped value>)."""
        return f"{type(self).__name__}({self.attr!r})"


class ID(Attr[str]):
    """Wrapper for a data-spec ID."""

    pass


class Name(Attr[Hashable]):
    """Wrapper for a data-spec name."""

    pass


class Tag(Attr[str]):
    """Wrapper for a data-spec tag."""

    pass


class Type(Attr[Any]):
    """Wrapper for a data-spec type."""

    pass


class Unit(Attr[Optional[str]]):
    """Wrapper for a data-spec unit."""

    pass


class Value(Attr[Optional[Any]]):
    """Wrapper for a data-spec value."""

    pass


def is_attr(obj: Any, /) -> TypeGuard[Attr[Any]]:
    """Check if given object is a wrapped data-spec attribute."""
    return isinstance(obj, Attr)


def is_id(obj: Any, /) -> TypeGuard[ID]:
    """Check if given object is a wrapped data-spec ID."""
    return isinstance(obj, ID)


def is_name(obj: Any, /) -> TypeGuard[Name]:
    """Check if given object is a wrapped data-spec name."""
    return isinstance(obj, Name)


def is_tag(obj: Any, /) -> TypeGuard[Tag]:
    """Check if given object is a wrapped data-spec tag."""
    return isinstance(obj, Tag)


def is_type(obj: Any, /) -> TypeGuard[Type]:
    """Check if given object is a wrapped data-spec type."""
    return isinstance(obj, Type)


def is_unit(obj: Any, /) -> TypeGuard[Unit]:
    """Check if given object is a wrapped data-spec unit."""
    return isinstance(obj, Unit)


def is_value(obj: Any, /) -> TypeGuard[Value]:
    """Check if given object is a wrapped data-spec value."""
    return isinstance(obj, Value)
