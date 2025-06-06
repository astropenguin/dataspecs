__all__ = ["ID", "ROOT", "Data", "Name", "Spec", "Specs", "Tag", "Type"]


# standard library
from abc import ABC, abstractmethod
from collections import UserList, defaultdict
from collections.abc import Hashable
from dataclasses import dataclass, field, replace
from os import fspath
from os.path import normpath
from pathlib import PurePosixPath as Path
from re import fullmatch
from typing import (
    Any,
    Generic,
    Literal,
    Optional,
    SupportsIndex,
    TypeVar,
    Union,
    overload,
)


# dependencies
from typing_extensions import Self, TypeGuard
from .typing import StrPath


# type hints
TAny = TypeVar("TAny")
TSpec = TypeVar("TSpec", bound="Spec[Any]")


# constants
ROOT = Path("/")


@dataclass(frozen=True)
class Spec(Generic[TAny]):
    """Data specification (dataspec)."""

    data: TAny = field(repr=False)
    """Data object of the dataspec."""

    id: Path = ROOT
    """POSIX path-like ID of the dataspec."""

    name: Hashable = None
    """Hashable name of the dataspec."""

    tags: frozenset[str] = frozenset()
    """Multiple string tags of the dataspec."""

    type: Any = Any
    """Data type of the dataspec."""

    def __post_init__(self) -> None:
        object.__setattr__(self, "id", Path(normpath(self.id)))
        object.__setattr__(self, "tags", frozenset(self.tags))


class Specs(UserList[TSpec]):
    """List of data specifications (dataspecs)."""

    @property
    def first(self) -> Optional[TSpec]:
        """Return the first dataspec if it exists (``None`` otherwise)."""
        return self[0] if len(self) else None

    @property
    def last(self) -> Optional[TSpec]:
        """Return the last dataspec if it exists (``None`` otherwise)."""
        return self[-1] if len(self) else None

    @property
    def unique(self) -> Optional[TSpec]:
        """Return the dataspec if it is unique (``None`` otherwise)."""
        return self[0] if len(self) == 1 else None

    def groupby(
        self,
        name: Literal["data", "id", "name", "tags", "type"],
        /,
    ) -> list[Self]:
        """Group the dataspecs by their attributes."""
        groups: defaultdict[Hashable, Self] = defaultdict(type(self))

        for spec in self:
            groups[getattr(spec, name)].append(spec)

        return list(groups.values())

    def merge(self) -> Self:
        """Merge the dataspecs of the same ID into single dataspec."""
        merged = type(self)()

        for group in self.groupby("id"):
            specifiers = group[Data(Specifier, type=True)]

            if (main := (group - specifiers).unique) is None:
                raise ValueError("Cannot identify main dataspec to merge.")

            for specifier in specifiers:
                main = main << specifier.data

            merged.append(main)

        return merged

    @overload
    def __getitem__(self, index: "Specifier[Any]", /) -> Self: ...

    @overload
    def __getitem__(self, index: slice, /) -> Self: ...

    @overload
    def __getitem__(self, index: SupportsIndex, /) -> TSpec: ...

    def __getitem__(
        self,
        index: Union["Specifier[Any]", slice, SupportsIndex],
        /,
    ) -> Union[Self, TSpec]:
        """Select the dataspecs by given index or specifier."""
        if Specifier.istype(index):
            return type(self)(spec for spec in self if index @ spec)
        else:
            return super().__getitem__(index)  # type: ignore

    def __sub__(self, other: Self, /) -> Self:
        """Return the dataspecs with given ones removed."""
        return type(self)(spec for spec in self if spec not in other)


@dataclass(frozen=True)
class Specifier(ABC, Generic[TAny]):
    """Specifier for dataspec's attributes."""

    value: TAny
    """Value to be set to or compared with dataspec's attributes."""

    regex: bool = False
    """Whether to compare the value by regular expression."""

    type: bool = False
    """Whether to compare the value by type inheritance."""

    @classmethod
    def istype(cls, obj: Any, /) -> TypeGuard[Self]:
        """Check if given object is an instance of the specifier."""
        return isinstance(obj, cls)

    @abstractmethod
    def __matmul__(self, spec: Spec[Any], /) -> bool:
        """Check if the value is equal to given dataspec's attribute."""
        pass

    @abstractmethod
    def __rshift__(self, spec: TSpec, /) -> TSpec:
        """Set the value to given dataspec's attribute."""
        pass

    def __rlshift__(self, spec: TSpec, /) -> TSpec:
        """Set the value to given dataspec's attribute."""
        return self.__rshift__(spec)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.value!r})"

    def __post_init__(self) -> None:
        if self.regex and self.type:
            raise ValueError("Regex and type cannot be True together.")


class Data(Specifier[Any]):
    def __rshift__(self, spec: TSpec, /) -> TSpec:
        """Set the value to given dataspec's data."""
        return replace(spec, data=self.value)

    def __matmul__(self, spec: Spec[Any], /) -> bool:
        """Check if the value is equal to given dataspec's data."""
        if self.regex:
            return (
                isinstance(self.value, str)
                and isinstance(spec.data, str)
                and bool(fullmatch(self.value, spec.data))
            )

        if self.type:
            return (
                isinstance(self.value, type)
                and isinstance(spec.data, object)
                and isinstance(spec.data, self.value)
            )

        return self.value == spec.data


class ID(Specifier[StrPath]):
    def __rshift__(self, spec: TSpec, /) -> TSpec:
        """Set the value to given dataspec's ID."""
        return replace(spec, id=Path(self.value))

    def __matmul__(self, spec: Spec[Any], /) -> bool:
        """Check if the value is equal to given dataspec's ID."""
        if self.regex:
            return bool(fullmatch(fspath(self.value), fspath(spec.id)))

        if self.type:
            raise ValueError("Type comparison is not supported.")

        return fspath(self.value) == fspath(spec.id)


class Name(Specifier[Hashable]):
    def __rshift__(self, spec: TSpec, /) -> TSpec:
        """Set the value to given dataspec's name."""
        return replace(spec, name=self.value)

    def __matmul__(self, spec: Spec[Any], /) -> bool:
        """Check if the value is equal to given dataspec's name."""
        if self.regex:
            return (
                isinstance(self.value, str)
                and isinstance(spec.name, str)
                and bool(fullmatch(self.value, spec.name))
            )

        if self.type:
            return (
                isinstance(self.value, type)
                and isinstance(spec.name, object)
                and isinstance(spec.name, self.value)
            )

        return self.value == spec.name


class Tag(Specifier[str]):
    def __rshift__(self, spec: TSpec, /) -> TSpec:
        """Add the value to given dataspec's tags."""
        return replace(spec, tags=(spec.tags | {self.value}))

    def __matmul__(self, spec: Spec[Any], /) -> bool:
        """Check if the value is contained in given dataspec's tag."""
        if self.regex:
            return any(fullmatch(self.value, tag) for tag in spec.tags)

        if self.type:
            raise ValueError("Type comparison is not supported.")

        return self.value in spec.tags


class Type(Specifier[Any]):
    def __rshift__(self, spec: TSpec, /) -> TSpec:
        """Set the value to given dataspec's type."""
        return replace(spec, type=self.value)

    def __matmul__(self, spec: Spec[Any], /) -> bool:
        """Check if the value is equal to given dataspec's type."""
        if self.regex:
            raise ValueError("Regex comparison is not supported.")

        if self.type:
            return (
                isinstance(self.value, type)
                and isinstance(spec.type, type)
                and issubclass(spec.type, self.value)
            )

        return self.value == spec.type
