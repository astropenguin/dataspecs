__all__ = ["ROOT", "Path", "Spec", "Specs"]


# standard library
from collections import UserList, defaultdict
from dataclasses import dataclass, field, replace
from os import fspath
from pathlib import PurePosixPath
from re import fullmatch
from typing import (
    Any,
    Callable,
    Generic,
    Hashable,
    Literal,
    Optional,
    SupportsIndex,
    TypeVar,
    overload,
)


# dependencies
from typing_extensions import Self
from .typing import (
    StrPath,
    TAny,
    UAny,
    TagBase,
    is_anytype,
    is_strpath,
    is_tag,
    is_tagtype,
)


# type hints
SpecAttr = Literal[
    "path",
    "name",
    "tags",
    "type",
    "data",
    "annotations",
    "metadata",
    "origin",
]
TSpec = TypeVar("TSpec", bound="Spec[Any]")


# constants
ROOT_PATH = "/"


class Path(PurePosixPath):
    """Path for data specs.

    It is based on ``PurePosixPath``, however,
    the differences are a path must start with the root (``/``)
    and the ``match`` method full-matches a regular expression.

    Args:
        *segments: Segments to create a path.

    Raises:
        ValueError: Raised if it does not start with the root.

    """

    # Implementation of __new__ is essential because
    # PurePosixPath does not implement __init__ in Python < 3.12.
    def __new__(cls, *segments: StrPath) -> Self:
        if PurePosixPath(*segments).root != ROOT_PATH:
            raise ValueError("Path must start with the root (/).")

        return super().__new__(cls, *segments)

    @property
    def children(self) -> Self:
        """Return the regular expression that matches the child paths."""
        return self / "[^/]+"

    @property
    def descendants(self) -> Self:
        """Return the regular expression that matches the descendant paths."""
        return self / ".+"

    def match(self, pattern: StrPath, /) -> bool:
        """Check if the path full-matches a regular expression."""
        return bool(fullmatch(fspath(pattern), fspath(self)))


ROOT = Path(ROOT_PATH)
"""Root path."""


@dataclass(frozen=True)
class Spec(Generic[TAny]):
    """Data specification (data spec).

    Args:
        path: Path of the data spec.
        name: Name of the data spec.
        tags: Tags of the data spec.
        type: Type hint for the data of the data spec.
        data: Default or final data of the data spec.
        annotations: Type hint annotations of the data spec.
        metadata: Metadata of the data spec.
        origin: Origin of the data spec.

    """

    path: Path
    """Path of the data spec."""

    name: Hashable
    """Name of the data spec."""

    tags: tuple[TagBase, ...]
    """Tags of the data spec."""

    type: Any
    """Type hint for the data of the data spec."""

    data: TAny
    """Default or final data of the data spec."""

    annotations: tuple[Any, ...] = field(default_factory=tuple, repr=False)
    """Type hint annotations of the data spec."""

    metadata: dict[str, Any] = field(default_factory=dict, repr=False)
    """Metadata of the data spec."""

    origin: Optional[Any] = field(default=None, repr=False)
    """Origin of the data spec."""

    def __call__(self, type: Callable[..., UAny], /) -> "Spec[UAny]":
        """Dynamically cast the data of the data spec."""
        return replace(self, data=type(self.data))  # type: ignore

    def __getitem__(self, type: Callable[..., UAny], /) -> "Spec[UAny]":
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

    def groupby(
        self,
        by: SpecAttr,
        /,
        *,
        method: Literal["eq", "equality", "id", "identity"] = "equality",
    ) -> list[Self]:
        """Group the data specs by their attributes.

        Args:
            by: Name of the data spec attribute for grouping.
                Either ``'path'``, ``'name'``, ``'tags'``, ``'type'``, ``'data'``,
                ``'annotations'``, ``'metadata'``, or ``'origin'`` is accepted.
            method: Grouping method.
                Either ``'equality'`` (or ``'eq'``; hash-based grouping),
                or ``'identity'`` (or ``'id'``; id-based grouping) is accepted.

        Returns:
            List of data specs grouped by the selected data spec attribute.

        """
        groups: defaultdict[Hashable, Self] = defaultdict(type(self))

        for spec in self:
            if method == "eq" or method == "equality":
                groups[getattr(spec, by)].append(spec)
            elif method == "id" or method == "identity":
                groups[id(getattr(spec, by))].append(spec)
            else:
                raise ValueError("Method must be either equality or identity.")

        return list(groups.values())

    def replace(self, old: TSpec, new: TSpec, /) -> Self:
        """Return data specs with old data spec replaced by new one."""
        return type(self)(new if spec == old else spec for spec in self)

    @overload
    def __getitem__(self, index: None, /) -> Self: ...

    @overload
    def __getitem__(self, index: TagBase, /) -> Self: ...

    @overload
    def __getitem__(self, index: type[Any], /) -> Self: ...

    @overload
    def __getitem__(self, index: StrPath, /) -> Self: ...

    @overload
    def __getitem__(self, index: slice, /) -> Self: ...

    @overload
    def __getitem__(self, index: SupportsIndex, /) -> TSpec: ...

    def __getitem__(self, index: Any, /) -> Any:
        """Select data specs with given index.

        In addition to a normal index (i.e. an object that has ``__index__`` method),
        it also accepts the following extended index for the advanced selection:
        (1) a tag to select data specs that contain it,
        (2) a tag type to select data specs that contain its tags,
        (3) an any type to select data specs that contain it,
        (4) a string path to select data specs that match it, or
        (5) ``None`` to return all data specs (shallow copy).

        Args:
            index: Normal or extended index for the selection of the data specs.

        Returns:
            Selected data specs with given index.

        """
        if is_tag(index):
            return type(self)(spec for spec in self if (index in spec.tags))

        if is_tagtype(index):
            return type(self)(
                spec
                for spec in self
                if any(isinstance(tag, index) for tag in spec.tags)
            )

        if is_anytype(index):
            return type(self)(
                spec
                for spec in self
                if isinstance(spec.type, type) and issubclass(spec.type, index)
            )

        if is_strpath(index):
            return type(self)(spec for spec in self if spec.path.match(index))

        if index is None:
            return self.copy()  # shallow copy

        return super().__getitem__(index)  # type: ignore
