__all__ = ["ID", "ROOT", "Spec", "Specs"]


# standard library
from collections import UserList
from collections.abc import Iterable
from dataclasses import dataclass, field
from os import fspath
from pathlib import PurePosixPath
from re import Match, compile, escape, fullmatch
from typing import Any, Optional, SupportsIndex, TypeVar, cast, overload


# dependencies
from typing_extensions import Self
from .typing import StrPath, TagBase, is_strpath, is_tag


# constants
GLOB_PATTERN = compile(r"\\\*\\\*()|\\\*([^\\\*]|$)|\\\?()")
GLOB_REPLS = r".*", r"[^/]*", r"[/_]"
ROOT_PATH = "/"


# type hints
TSpec = TypeVar("TSpec", bound="Spec")


class ID(PurePosixPath):
    """Identifier (ID) for data specs.

    It is based on ``PurePosixPath``, however,
    the difference is an ID must start with the root (``/``).

    Args:
        *segments: Path segments to create an ID.

    Raises:
        ValueError: Raised if it does not start with the root.

    """

    # Implementation of __new__ is essential because PurePosixPath
    # does not implement __init__ prior to Python 3.12.
    def __new__(cls, *segments: StrPath) -> Self:
        if PurePosixPath(*segments).root != ROOT_PATH:
            raise ValueError("ID must start with the root.")

        return super().__new__(cls, *segments)

    def match(self, path_pattern: StrPath, /) -> bool:
        """Check if the ID matches a path pattern.

        Unlike original ``PurePosixPath.match``, it always performs
        case-sensitive matching. It also accepts double-wildcards
        (``**``) for recursively matching the path segments
        and question mark (``?``) for matching ``/`` or ``_``.

        Args:
            path_pattern: Path pattern for matching.

        Returns:
            ``True`` if the path pattern matches the ID.
            ``False`` otherwise.

        """

        def repl(match: Match[str]) -> str:
            index = cast(int, match.lastindex)
            return GLOB_REPLS[index - 1] + match.group(index)

        regex = GLOB_PATTERN.sub(repl, escape(fspath(path_pattern)))
        return bool(fullmatch(regex, fspath(self)))


ROOT = ID("/")
"""Root ID."""


@dataclass(frozen=True)
class Spec:
    """Data specification (data spec).

    Args:
        id: ID of the data spec.
        tags: Tags of the data spec.
        data: Data of the data spec.
        type: Type hint of the data spec.
        origin: Origin of the data spec.

    """

    id: ID
    """ID of the data spec."""

    tags: tuple[TagBase, ...]
    """Tags of the data spec."""

    data: Any
    """Data of the data spec."""

    type: Any = field(default=Any, repr=False)
    """Type hint of the data spec."""

    origin: Any = field(default=None, repr=False)
    """Origin of the data spec."""


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

    @overload
    def __getitem__(self, index: None, /) -> Self: ...

    @overload
    def __getitem__(self, index: TagBase, /) -> Self: ...

    @overload
    def __getitem__(self, index: StrPath, /) -> Self: ...

    @overload
    def __getitem__(self, index: SupportsIndex, /) -> TSpec: ...

    @overload
    def __getitem__(self, index: slice, /) -> Self: ...

    def __getitem__(self, index: Any, /) -> Any:
        """Select data specs with given index.

        In addition to the normal list indexing, it also accepts
        (1) a tag to select data specs that contain it,
        (2) a string path to select data specs that match it, or
        (3) ``None`` to return all data specs (shallow copy).

        Args:
            index: Index for selection. Either a normal index
                (i.e. an object that has ``__index__`` method),
                a tag, a string path, or ``None`` is accepted.

        Returns:
            Selected data specs with given index.

        """
        if index is None:
            return self.copy()  # shallow copy

        if is_tag(index):
            return type(self)(spec for spec in self if (index in spec.tags))

        if is_strpath(index):
            return type(self)(spec for spec in self if spec.id.match(index))

        return super().__getitem__(index)  # type: ignore

    def __sub__(self, removed: Iterable[TSpec], /) -> Self:
        """Return data specs with given ones removed.

        Args:
            removed: Data specs to be removed.

        Returns:
            Data specs with given data specs removed.

        """
        return type(self)(spec for spec in self if (spec not in removed))
