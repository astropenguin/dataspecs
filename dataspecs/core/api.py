__all__ = ["from_dataclass", "from_typehint"]


# standard library
from dataclasses import fields
from typing import Any, Callable, overload


# dependencies
from .specs import ID, ROOT, Spec, Specs, TSpec
from .typing import (
    DataClass,
    StrPath,
    get_annotated,
    get_dataclasses,
    get_first,
    get_subtypes,
    get_tags,
)


@overload
def from_dataclass(
    obj: DataClass,
    /,
    *,
    first_only: bool = True,
    tagged_only: bool = True,
    type_only: bool = True,
    parent_id: StrPath = ROOT,
) -> Specs[Spec[Any]]: ...


@overload
def from_dataclass(
    obj: DataClass,
    /,
    *,
    first_only: bool = True,
    tagged_only: bool = True,
    type_only: bool = True,
    parent_id: StrPath = ROOT,
    spec_factory: Callable[..., TSpec],
) -> Specs[TSpec]: ...


def from_dataclass(
    obj: DataClass,
    /,
    *,
    first_only: bool = True,
    tagged_only: bool = True,
    type_only: bool = True,
    parent_id: StrPath = ROOT,
    spec_factory: Any = Spec,
) -> Any:
    """Create data specs from a dataclass (object).

    Args:
        obj: Dataclass (object) to be parsed.
        first_only: If ``True`` and a type hint is a union of types,
            parse the first type only instead of the whole type hint.
        tagged_only: If ``True``, drop leaf (i.e. terminal) and
            adjacent superior data specs that do not have any tags.
        type_only: If ``True``, each data spec type contains
            a type hint with all annotation removed.
        parent_id: ID of the parent data spec.
        spec_factory: Factory for creating each data spec.

    Returns:
        Data specs created from the dataclass (object).

    """
    specs: Specs[Any] = Specs()

    for field in fields(obj):
        specs.extend(
            from_typehint(
                field.type,
                first_only=first_only,
                tagged_only=tagged_only,
                type_only=type_only,
                parent_id=ID(parent_id) / field.name,
                parent_data=getattr(obj, field.name, field.default),
                spec_factory=spec_factory,
            )
        )

    return specs


@overload
def from_typehint(
    obj: Any,
    /,
    *,
    first_only: bool = True,
    tagged_only: bool = True,
    type_only: bool = True,
    parent_id: StrPath = ROOT,
    parent_data: Any = None,
) -> Specs[Spec[Any]]: ...


@overload
def from_typehint(
    obj: Any,
    /,
    *,
    first_only: bool = True,
    tagged_only: bool = True,
    type_only: bool = True,
    parent_id: StrPath = ROOT,
    parent_data: Any = None,
    spec_factory: Callable[..., TSpec],
) -> Specs[TSpec]: ...


def from_typehint(
    obj: Any,
    /,
    *,
    first_only: bool = True,
    tagged_only: bool = True,
    type_only: bool = True,
    parent_id: StrPath = ROOT,
    parent_data: Any = None,
    spec_factory: Any = Spec,
) -> Any:
    """Create data specs from a type hint.

    Args:
        obj: Type hint to be parsed.
        first_only: If ``True`` and a type hint is a union of types,
            parse the first type only instead of the whole type hint.
        tagged_only: If ``True``, drop leaf (i.e. terminal) and
            adjacent superior data specs that do not have any tags.
        type_only: If ``True``, each data spec type contains
            a type hint with all annotation removed.
        parent_id: ID of the parent data spec.
        parent_data: Data of the parent data spec.
        spec_factory: Factory for creating each data spec.

    Returns:
        Data specs created from the type hint.

    """
    specs: Specs[Any] = Specs()

    if first_only:
        obj = get_first(obj)

    specs.append(
        spec_factory(
            id=ID(parent_id),
            tags=get_tags(obj),
            type=get_annotated(obj, True) if type_only else obj,
            data=parent_data,
        )
    )

    for index, subtype in enumerate(get_subtypes(obj)):
        specs.extend(
            from_typehint(
                subtype,
                first_only=first_only,
                tagged_only=tagged_only,
                type_only=type_only,
                parent_id=ID(parent_id) / str(index),
                spec_factory=spec_factory,
            )
        )

    for dc in get_dataclasses(obj):
        specs.extend(
            from_dataclass(
                dc,
                first_only=first_only,
                tagged_only=tagged_only,
                type_only=type_only,
                parent_id=ID(parent_id),
                spec_factory=spec_factory,
            )
        )

    return drop_leaves(specs) if tagged_only else specs


def drop_leaves(specs: Specs[TSpec], /) -> Specs[TSpec]:
    """Drop leaf specs that do not have any tags."""
    dropped = specs.copy()

    for spec in specs:
        if not spec.tags and not specs[spec.id / "[^/]+"]:
            dropped.remove(spec)

    return dropped
