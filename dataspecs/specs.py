__all__ = ["Spec", "Specs"]


# standard library
from dataclasses import dataclass, field
from typing import Any, Optional, SupportsIndex, overload


# dependencies
from typing_extensions import Self
from .typing import ID, StrPath, TagBase, is_strpath, is_tag


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


class Specs(list[Spec]):
    """Data specifications (data specs)."""

    @property
    def first(self) -> Optional[Spec]:
        """Return the first data spec if it exists (``None`` otherwise)."""
        return self[0] if len(self) else None

    @property
    def last(self) -> Optional[Spec]:
        """Return the last data spec if it exists (``None`` otherwise)."""
        return self[-1] if len(self) else None

    @overload
    def __getitem__(self, index: TagBase, /) -> Self: ...

    @overload
    def __getitem__(self, index: StrPath, /) -> Self: ...

    @overload
    def __getitem__(self, index: SupportsIndex, /) -> Spec: ...

    @overload
    def __getitem__(self, index: slice, /) -> Self: ...

    def __getitem__(self, index: Any, /) -> Any:
        """Select data specs with given index.

        In addition to normal list indexing, it also accepts
        (1) a tag to select data specs that contain it and
        (2) a string path to select data specs that match it.

        Args:
            index: Index for selection. Either a normal index
                (i.e. an object that has ``__index__`` method),
                a tag, or a string path is accepted.

        Returns:
            Selected data specs with given index.

        Raises:
            TypeError: Raised if the index type is not supported.

        """
        cls = type(self)

        if is_tag(index):
            return cls([spec for spec in self if index in spec.tags])

        if is_strpath(index):
            return cls([spec for spec in self if spec.id.matches(index)])

        if isinstance(index, (SupportsIndex, slice)):
            return super().__getitem__(index)

        raise TypeError(f"Index type {type(index)!r} is not supported.")
