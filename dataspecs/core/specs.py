__all__ = ["Of", "Specs"]


# standard library
from collections import UserList, defaultdict
from collections.abc import Hashable
from dataclasses import dataclass
from typing import Any, Literal, Optional, SupportsIndex, TypeVar, Union, overload


# dependencies
from typing_extensions import Self
from .spec import Data, Spec, Specifier


# type hints
TSpec = TypeVar("TSpec", bound=Spec[Any])


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

    def groupby(
        self,
        name: Literal["data", "id", "name", "tags", "type", "unit"],
        /,
    ) -> list[Self]:
        """Group the dataspecs by their attributes."""
        groups: defaultdict[Hashable, Self] = defaultdict(type(self))

        for spec in self:
            groups[getattr(spec, name)].append(spec)

        return list(groups.values())

    def merge(self) -> Self:
        """Merge the dataspecs with the same ID."""
        merged = type(self)()

        for group in self.groupby("id"):
            specifiers = group[Data(Of(Specifier))]

            if (main := (group - specifiers).unique) is None:
                raise ValueError("")

            for specifier in specifiers:
                main = main << specifier.data

            merged.append(main)

        return merged

    def replace(self, old: TSpec, new: TSpec, /) -> Self:
        """Return dataspecs with old dataspec replaced by new one."""
        return type(self)(new if spec == old else spec for spec in self)

    @overload
    def __getitem__(self, index: Specifier[Any], /) -> Self: ...

    @overload
    def __getitem__(self, index: slice, /) -> Self: ...

    @overload
    def __getitem__(self, index: SupportsIndex, /) -> TSpec: ...

    def __getitem__(
        self,
        index: Union[Specifier[Any], slice, SupportsIndex],
        /,
    ) -> Union[Self, TSpec]:
        """Select the dataspecs by given index or wrapped attribute."""
        if Specifier.istype(index):
            return type(self)(spec for spec in self if index @ spec)
        else:
            return super().__getitem__(index)  # type: ignore

    def __sub__(self, other: Self, /) -> Self:
        """Return the dataspecs with given ones removed."""
        return type(self)(spec for spec in self if spec not in other)


@dataclass(frozen=True)
class Of:
    """"""

    type: Any

    def __eq__(self, other: Any, /) -> bool:
        if isinstance(other, type):
            return issubclass(other, self.type)
        else:
            return isinstance(other, self.type)
