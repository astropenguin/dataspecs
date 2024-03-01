__all__ = ["ID", "ROOT", "Spec", "Specs"]


# standard library
from dataclasses import dataclass, field
from os import fspath
from pathlib import PurePosixPath
from re import Match, compile, escape, fullmatch
from typing import Any, Optional, SupportsIndex, TypeVar, cast, overload


# dependencies
from typing_extensions import Self
from .typing import StrPath, TagBase, is_strpath, is_tag


# constants
GLOB_PATTERN = compile(r"\\\*\\\*()|\\\*([^\\\*]|$)")
GLOB_REPLS = r".*", r"[^/]*"


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

    def __init__(self, *segments: StrPath) -> None:
        super().__init__(*segments)

        if not self.root:
            raise ValueError("ID must start with the root.")

    def matches(self, path_pattern: StrPath, /) -> bool:
        """Check if the ID matches a path pattern.

        Unlike ``ID.match``, it also accepts double-wildcards
        (``**``) for recursively matching the path segments.

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
        type: Type hint of the data spec.
        data: Data of the data spec.
        origin: Origin of the data spec.

    """

    id: ID
    """ID of the data spec."""

    tags: tuple[TagBase, ...]
    """Tags of the data spec."""

    type: Any = field(repr=False)
    """Type hint of the data spec."""

    data: Any = field(repr=False)
    """Data of the data spec."""

    origin: Any = field(repr=False)
    """Origin of the data spec."""


class Specs(list[TSpec]):
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

        Raises:
            TypeError: Raised if the index type is not supported.

        """
        cls = type(self)

        if index is None:
            return cls(self)  # shallow copy

        if is_tag(index):
            return cls([spec for spec in self if index in spec.tags])

        if is_strpath(index):
            return cls([spec for spec in self if spec.id.matches(index)])

        if isinstance(index, SupportsIndex):
            return super().__getitem__(index)

        if isinstance(index, slice):
            return cls(super().__getitem__(index))

        raise TypeError(f"Index type {type(index)!r} is not supported.")
