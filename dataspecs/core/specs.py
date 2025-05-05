__all__ = ["Specs"]


# standard library
from collections import UserList, defaultdict
from typing import (
    Any,
    Hashable,
    Literal,
    Optional,
    SupportsIndex,
    TypeVar,
    Union,
    overload,
)


# dependencies
from typing_extensions import Self
from .spec import Attr, Spec, is_data, is_id, is_name, is_tag, is_type, is_unit


# type hints
TSpec = TypeVar("TSpec", bound=Spec[Any])
AttrName = Literal["data", "id", "name", "tags", "type", "unit"]
SpecsIndex = Union[Attr[Any], slice, SupportsIndex]


class Specs(UserList[TSpec]):
    """Data specifications (dataspecs)."""

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

    def groupby(self, attr: AttrName, /) -> list[Self]:
        """Group the dataspecs by their attributes."""
        groups: defaultdict[Hashable, Self] = defaultdict(type(self))

        for spec in self:
            groups[getattr(spec, attr)].append(spec)

        return list(groups.values())

    def replace(self, old: TSpec, new: TSpec, /) -> Self:
        """Return dataspecs with old dataspec replaced by new one."""
        return type(self)(new if spec == old else spec for spec in self)

    @overload
    def __getitem__(self, index: Attr[Any], /) -> Self: ...

    @overload
    def __getitem__(self, index: slice, /) -> Self: ...

    @overload
    def __getitem__(self, index: SupportsIndex, /) -> TSpec: ...

    def __getitem__(self, index: SpecsIndex, /) -> Union[Self, TSpec]:
        """Select the dataspecs by given index or wrapped attribute."""
        if is_data(index):
            return type(self)(spec for spec in self if index.attr == spec.data)

        if is_id(index):
            return type(self)(spec for spec in self if index.attr == spec.id)

        if is_name(index):
            return type(self)(spec for spec in self if index.attr == spec.name)

        if is_tag(index):
            return type(self)(spec for spec in self if index.attr in spec.tags)

        if is_type(index):
            return type(self)(spec for spec in self if index.attr == spec.type)

        if is_unit(index):
            return type(self)(spec for spec in self if index.attr == spec.unit)

        return super().__getitem__(index)  # type: ignore
