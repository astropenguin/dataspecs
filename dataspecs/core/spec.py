__all__ = ["Attr", "Data", "ID", "Name", "Spec", "Tag", "Type", "Unit"]


# standard library
from collections.abc import Hashable
from dataclasses import dataclass, field
from typing import Any, Generic, Optional, TypeVar


# dependencies
from typing_extensions import TypeGuard


# type hints
TAny = TypeVar("TAny")


@dataclass(frozen=True)
class Spec(Generic[TAny]):
    """Data specification (dataspec)."""

    data: TAny = field(repr=False)
    """Dataspec data."""

    id: str
    """Dataspec ID."""

    name: Hashable
    """Dataspec name."""

    tags: frozenset[str]
    """Dataspec tags."""

    type: Any
    """Type of the dataspec data."""

    unit: Optional[str]
    """Unit of the dataspec data."""

    @property
    def data_(self) -> "Data":
        """Wrapped dataspec data."""
        return Data(self.data)

    @property
    def id_(self) -> "ID":
        """Wrapped dataspec ID."""
        return ID(self.id)

    @property
    def name_(self) -> "Name":
        """Wrapped dataspec name."""
        return Name(self.name)

    @property
    def tags_(self) -> frozenset["Tag"]:
        """Wrapped dataspec tags."""
        return frozenset(Tag(tag) for tag in self.tags)

    @property
    def type_(self) -> "Type":
        """Wrapped type of the dataspec data."""
        return Type(self.type)

    @property
    def unit_(self) -> "Unit":
        """Wrapped unit of the dataspec data."""
        return Unit(self.unit)


class Attr(Generic[TAny]):
    """Wrapper for dataspec attributes."""

    def __init__(self, attr: TAny, /) -> None:
        self.attr = attr

    def __repr__(self) -> str:
        """Return string of <class name>(<wrapped value>)."""
        return f"{type(self).__name__}({self.attr!r})"


class Data(Attr[Any]):
    """Wrapper for a dataspec data."""

    pass


class ID(Attr[str]):
    """Wrapper for a dataspec ID."""

    pass


class Name(Attr[Hashable]):
    """Wrapper for a dataspec name."""

    pass


class Tag(Attr[str]):
    """Wrapper for a dataspec tag."""

    pass


class Type(Attr[Any]):
    """Wrapper for a dataspec type."""

    pass


class Unit(Attr[Optional[str]]):
    """Wrapper for a dataspec unit."""

    pass


def is_attr(obj: Any, /) -> TypeGuard[Attr[Any]]:
    """Check if given object is a wrapped dataspec attribute."""
    return isinstance(obj, Attr)


def is_data(obj: Any, /) -> TypeGuard[Data]:
    """Check if given object is a wrapped dataspec data."""
    return isinstance(obj, Data)


def is_id(obj: Any, /) -> TypeGuard[ID]:
    """Check if given object is a wrapped dataspec ID."""
    return isinstance(obj, ID)


def is_name(obj: Any, /) -> TypeGuard[Name]:
    """Check if given object is a wrapped dataspec name."""
    return isinstance(obj, Name)


def is_tag(obj: Any, /) -> TypeGuard[Tag]:
    """Check if given object is a wrapped dataspec tag."""
    return isinstance(obj, Tag)


def is_type(obj: Any, /) -> TypeGuard[Type]:
    """Check if given object is a wrapped dataspec type."""
    return isinstance(obj, Type)


def is_unit(obj: Any, /) -> TypeGuard[Unit]:
    """Check if given object is a wrapped dataspec unit."""
    return isinstance(obj, Unit)
