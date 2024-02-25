__all__ = ["Spec", "Specs"]


# standard library
from dataclasses import dataclass, field, fields
from typing import Any


# dependencies
from typing_extensions import Self
from .typing import (
    ID,
    ROOT,
    DataClass,
    StrPath,
    TagBase,
    get_annotated,
    get_dataclasses,
    get_subscriptions,
    get_tags,
)


@dataclass
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

    tags: list[TagBase]
    """Tags of the data spec."""

    type: Any = field(repr=False)
    """Type hint of the data spec."""

    data: Any = field(repr=False)
    """Data of the data spec."""

    origin: Any = field(repr=False)
    """Origin of the data spec."""


class Specs(list[Spec]):
    """Data specifications (data specs)."""

    @classmethod
    def from_dataclass(cls, dc: DataClass, parent: StrPath = ROOT) -> Self:
        """Create data specs from a dataclass object.

        Args:
            dc: Dataclass object to be parsed.
            parent: ID of the parent data spec.

        Returns:
            Data specs created from the dataclass object.

        """
        specs = cls()

        for f in fields(dc):
            spec = Spec(
                id=(id_ := ID(parent) / f.name),
                type=(annotated := get_annotated(f.type)),
                data=getattr(dc, f.name, f.default),
                tags=list(get_tags(f.type)),
                origin=dc,
            )

            specs.append(spec)
            specs.extend(cls.from_typehint(annotated, id_))

            for dc_ in get_dataclasses(f.type):
                specs.extend(cls.from_dataclass(dc_, id_))

        return specs

    @classmethod
    def from_typehint(cls, hint: Any, parent: StrPath = ROOT) -> Self:
        """Create data specs from a type hint.

        Args:
            hint: Type hint to be parsed.
            parent: ID of the parent data spec.

        Returns:
            Data specs created from the type hint.

        """
        specs = cls()

        for name, type_ in enumerate(get_subscriptions(hint)):
            spec = Spec(
                id=(id_ := ID(parent) / str(name)),
                type=Any,
                data=(annotated := get_annotated(type_)),
                tags=list(get_tags(type_)),
                origin=hint,
            )

            specs.append(spec)
            specs.extend(cls.from_typehint(annotated, id_))

            for dc_ in get_dataclasses(type_):
                specs.extend(cls.from_dataclass(dc_, id_))

        return specs
