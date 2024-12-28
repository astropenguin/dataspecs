__all__ = ["ID", "ROOT", "Spec", "Specs"]


# standard library
from collections import UserList
from dataclasses import dataclass, replace
from os import fspath
from os.path import commonpath
from pathlib import PurePosixPath
from re import fullmatch
from typing import (
    Any,
    Callable,
    Generic,
    Optional,
    SupportsIndex,
    TypeVar,
    Union,
    overload,
)


# dependencies
from typing_extensions import Self
from .typing import StrPath, TagBase, is_strpath, is_tag, is_tagtype


# type hints
ExtendedIndex = Union[TagBase, type[TagBase], StrPath, None]


# constants
ROOT_PATH = "/"


# type hints
S = TypeVar("S")
T = TypeVar("T")
TSpec = TypeVar("TSpec", bound="Spec[Any]")


class ID(PurePosixPath):
    """Identifier (ID) for data specs.

    It is based on ``PurePosixPath``, however,
    the difference is an ID must start with the root (``/``).

    Args:
        *segments: Path segments to create an ID.

    Raises:
        ValueError: Raised if it does not start with the root.

    """

    # Implementation of __new__ is essential because
    # PurePosixPath does not implement __init__ in Python < 3.12.
    def __new__(cls, *segments: StrPath) -> Self:
        if PurePosixPath(*segments).root != ROOT_PATH:
            raise ValueError("ID must start with the root (/).")

        return super().__new__(cls, *segments)

    def match(self, pattern: StrPath, /) -> bool:
        """Check if the ID full-matches a regular expression."""
        return bool(fullmatch(fspath(pattern), fspath(self)))


ROOT = ID(ROOT_PATH)
"""Root ID."""


@dataclass(frozen=True)
class Spec(Generic[T]):
    """Data specification (data spec).

    Args:
        id: ID of the data spec.
        tags: Tags of the data spec.
        type: Type hint for the data of the data spec.
        data: Default or final data of the data spec.

    """

    id: ID
    """ID of the data spec."""

    tags: tuple[TagBase, ...]
    """Tags of the data spec."""

    type: Any
    """Type hint for the data of the data spec."""

    data: T
    """Default or final data of the data spec."""

    def __call__(self, type: Callable[..., S], /) -> "Spec[S]":
        """Dynamically cast the data of the data spec."""
        return replace(self, data=type(self.data))  # type: ignore

    def __getitem__(self, type: Callable[..., S], /) -> "Spec[S]":
        """Statically cast the data of the data spec."""
        return self  # type: ignore


class Specs(UserList[TSpec]):
    """Data specifications (data specs)."""

    @property
    def first(self) -> Optional[TSpec]:
        """Return the first data spec if it exists (``None`` otherwise)."""
        return self[0] if len(self) else None

    @property
    def last(self) -> Optional[TSpec]:
        """Return the last data spec if it exists (``None`` otherwise)."""
        return self[-1] if len(self) else None

    @property
    def unique(self) -> Optional[TSpec]:
        """Return the data spec if it is unique (``None`` otherwise)."""
        return self[0] if len(self) == 1 else None

    def groups(self, index: ExtendedIndex = None, /) -> list[Self]:
        """Return list of data specs grouped by the common ID."""
        parent_id = ID(commonpath(spec.id for spec in self))

        return [
            self[f"{spec.id}(|/.*)"]
            for spec in self[index]
            if spec.id.parent == parent_id
        ]

    def replace(self, old: TSpec, new: TSpec, /) -> Self:
        """Return data specs with old data spec replaced by new one."""
        return type(self)(new if spec == old else spec for spec in self)

    @overload
    def __getitem__(self, index: None, /) -> Self: ...

    @overload
    def __getitem__(self, index: TagBase, /) -> Self: ...

    @overload
    def __getitem__(self, index: type[TagBase], /) -> Self: ...

    @overload
    def __getitem__(self, index: StrPath, /) -> Self: ...

    @overload
    def __getitem__(self, index: slice, /) -> Self: ...

    @overload
    def __getitem__(self, index: SupportsIndex, /) -> TSpec: ...

    def __getitem__(self, index: Any, /) -> Any:
        """Select data specs with given index.

        In addition to the normal list indexing, it also accepts
        (1) a tag to select data specs that contain it,
        (2) a tag type to select data specs that contain its tags,
        (3) a string path to select data specs that match it, or
        (4) ``None`` to return all data specs (shallow copy).

        Args:
            index: Index for selection. Either a normal index
                (i.e. an object that has ``__index__`` method),
                a tag, a tag type, a string path, or ``None`` is accepted.

        Returns:
            Selected data specs with given index.

        """
        if index is None:
            return self.copy()  # shallow copy

        if is_tag(index):
            return type(self)(spec for spec in self if (index in spec.tags))

        if is_tagtype(index):
            return type(self)(
                spec
                for spec in self
                if any(isinstance(tag, index) for tag in spec.tags)
            )

        if is_strpath(index):
            return type(self)(spec for spec in self if spec.id.match(index))

        return super().__getitem__(index)  # type: ignore
