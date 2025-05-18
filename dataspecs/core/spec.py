__all__ = ["Data", "ID", "Name", "Spec", "Tag", "Type", "Unit"]


# standard library
from abc import ABC, abstractmethod
from collections.abc import Hashable
from dataclasses import dataclass, field, replace
from os import PathLike, fspath
from os.path import normpath
from pathlib import PurePosixPath
from re import fullmatch
from typing import Any, Generic, Optional, TypeVar, Union


# dependencies
from typing_extensions import Self, TypeGuard


# type hints
TAny = TypeVar("TAny")
TSpec = TypeVar("TSpec", bound="Spec[Any]")


@dataclass(frozen=True)
class Spec(Generic[TAny]):
    """Data specification (dataspec)."""

    data: TAny = field(repr=False)
    """Dataspec data."""

    id: PurePosixPath
    """Dataspec ID."""

    name: Hashable = None
    """Dataspec name."""

    tags: frozenset[str] = frozenset()
    """Dataspec tags."""

    type: Any = Any
    """Type of the dataspec data."""

    unit: Optional[str] = None
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

    def __post_init__(self) -> None:
        super().__setattr__("id", PurePosixPath(normpath(self.id)))


@dataclass(frozen=True)
class Specifier(ABC, Generic[TAny]):
    """Specifier for dataspec's attributes."""

    value: TAny

    @classmethod
    def istype(cls, obj: Any, /) -> TypeGuard[Self]:
        """Check if given object is an instance of it."""
        return isinstance(obj, cls)

    @abstractmethod
    def __matmul__(self, spec: Spec[Any], /) -> bool:
        """Check if its value is in given dataspec."""
        pass

    @abstractmethod
    def __rshift__(self, spec: TSpec, /) -> TSpec:
        """Set its value to given dataspec's attribute."""
        pass

    def __rlshift__(self, spec: TSpec, /) -> TSpec:
        """Set its value to given dataspec's attribute."""
        return self >> spec

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.value!r})"


class Data(Specifier[Any]):
    def __rshift__(self, spec: TSpec, /) -> TSpec:
        """Set its value to given dataspecs' data."""
        return replace(spec, data=self.value)

    def __matmul__(self, spec: Spec[Any], /) -> bool:
        """Check if its value is in given dataspec."""
        return self.value == spec.data


class ID(Specifier[PurePosixPath]):
    def __init__(self, value: Union[PathLike[str], str], /) -> None:
        object.__setattr__(self, "value", PurePosixPath(value))

    def __rshift__(self, spec: TSpec, /) -> TSpec:
        """Set its value to given dataspecs' ID."""
        return replace(spec, id=self.value)

    def __matmul__(self, spec: Spec[Any], /) -> bool:
        """Check if its value is in given dataspec."""
        return bool(fullmatch(fspath(self.value), fspath(spec.id)))


class Name(Specifier[Hashable]):
    def __rshift__(self, spec: TSpec, /) -> TSpec:
        """Set its value to given dataspecs' name."""
        return replace(spec, name=self.value)

    def __matmul__(self, spec: Spec[Any], /) -> bool:
        """Check if its value is in given dataspec."""
        return self.value == spec.name


class Tag(Specifier[str]):
    def __rshift__(self, spec: TSpec, /) -> TSpec:
        """Add its value to given dataspecs' tags."""
        return replace(spec, tags=(spec.tags | {self.value}))

    def __matmul__(self, spec: Spec[Any], /) -> bool:
        """Check if its value is in given dataspec."""
        return self.value in spec.tags


class Type(Specifier[Any]):
    def __rshift__(self, spec: TSpec, /) -> TSpec:
        """Set its value to given dataspecs' type."""
        return replace(spec, type=self.value)

    def __matmul__(self, spec: Spec[Any], /) -> bool:
        """Check if its value is in given dataspec."""
        return self.value == spec.type


class Unit(Specifier[Optional[str]]):
    def __rshift__(self, spec: TSpec, /) -> TSpec:
        """Set its value to given dataspecs' unit."""
        return replace(spec, unit=self.value)

    def __matmul__(self, spec: Spec[Any], /) -> bool:
        """Check if its value is in given dataspec."""
        return self.value == spec.unit
