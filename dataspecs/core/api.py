__all__ = ["from_dataclass", "from_typehint"]


# standard library
from dataclasses import fields
from typing import Any, Callable, overload


# dependencies
from .specs import ID, ROOT, Spec, Specs, TSpec
from .typing import (
    DataClass,
    StrPath,
    get_dataclasses,
    get_final,
    get_first,
    get_subtypes,
    get_tags,
)


# constants
FIRST_ONLY = "_DATASPECS_FIRST_ONLY"
TAGGED_ONLY = "_DATASPECS_TAGGED_ONLY"
TYPE_ONLY = "_DATASPECS_TYPE_ONLY"


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
    """Create data specs from a dataclass object.

    Args:
        obj: Dataclass object to be parsed.
        first_only: If ``True`` and a type hint is a union of types,
            parse the first type only instead of the whole type hint.
            Note that if ``obj._DATASPECS_FIRST_ONLY`` exists,
            it will take precedence regardless of ``first_only``.
        tagged_only: If ``True``, drop leaf (i.e. terminal) and
            adjacent superior data specs that do not have any tags.
            Note that if ``obj._DATASPECS_TAGGED_ONLY`` exists,
            it will take precedence regardless of ``tagged_only``.
        type_only: If ``True``, each data spec type contains
            a type hint with all annotation removed.
            Note that if ``obj._DATASPECS_TYPE_ONLY`` exists,
            it will take precedence regardless of ``type_only``.
        parent_id: ID of the parent data spec.
        spec_factory: Factory for creating each data spec.

    Returns:
        Data specs created from the dataclass object.

    """
    first_only = getattr(obj, FIRST_ONLY, first_only)
    tagged_only = getattr(obj, TAGGED_ONLY, tagged_only)
    type_only = getattr(obj, TYPE_ONLY, type_only)

    specs: Specs[Any] = Specs()

    for field in fields(obj):
        reftype = get_first(field.type) if first_only else field.type

        specs.append(
            spec_factory(
                id=(child_id := ID(parent_id) / field.name),
                tags=get_tags(reftype),
                type=get_final(field.type, type_only),
                data=getattr(obj, field.name, field.default),
            )
        )
        specs.extend(
            from_typehint(
                reftype,
                first_only=first_only,
                tagged_only=tagged_only,
                type_only=type_only,
                parent_id=child_id,
                spec_factory=spec_factory,
            )
        )

    return drop_leaves(specs) if tagged_only else specs


@overload
def from_typehint(
    obj: Any,
    /,
    *,
    first_only: bool = True,
    tagged_only: bool = True,
    type_only: bool = True,
    parent_id: StrPath = ROOT,
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
    spec_factory: Any = Spec,
) -> Any:
    """Create data specs from a type hint.

    Args:
        obj: Type hint to be parsed.
        first_only: If ``True`` and a type hint is a union of types,
            parse the first type only instead of the whole type hint.
            Note that if ``obj._DATASPECS_FIRST_ONLY`` exists,
            it will take precedence regardless of ``first_only``.
        tagged_only: If ``True``, drop leaf (i.e. terminal) and
            adjacent superior data specs that do not have any tags.
            Note that if ``obj._DATASPECS_TAGGED_ONLY`` exists,
            it will take precedence regardless of ``tagged_only``.
        type_only: If ``True``, each data spec type contains
            a type hint with all annotation removed.
            Note that if ``obj._DATASPECS_TYPE_ONLY`` exists,
            it will take precedence regardless of ``type_only``.
        parent_id: ID of the parent data spec.
        spec_factory: Factory for creating each data spec.

    Returns:
        Data specs created from the type hint.

    """
    first_only = getattr(obj, FIRST_ONLY, first_only)
    tagged_only = getattr(obj, TAGGED_ONLY, tagged_only)
    type_only = getattr(obj, TYPE_ONLY, type_only)

    specs: Specs[Any] = Specs()

    for name, subtype in enumerate(get_subtypes(obj)):
        specs.append(
            spec_factory(
                id=(child_id := ID(parent_id) / str(name)),
                tags=get_tags(subtype),
                type=get_final(subtype, type_only),
                data=None,
            )
        )
        specs.extend(
            from_typehint(
                subtype,
                first_only=first_only,
                tagged_only=tagged_only,
                type_only=type_only,
                parent_id=child_id,
                spec_factory=spec_factory,
            )
        )

    for dataclass in get_dataclasses(obj):
        specs.extend(
            from_dataclass(
                dataclass,
                first_only=first_only,
                tagged_only=tagged_only,
                type_only=type_only,
                parent_id=parent_id,
                spec_factory=spec_factory,
            )
        )

    return drop_leaves(specs) if tagged_only else specs


def drop_leaves(specs: Specs[TSpec], /) -> Specs[TSpec]:
    """Drop leaf specs that do not have any tags."""
    dropped = specs.copy()

    for spec in specs:
        if not spec.tags and not specs[spec.id / "**"]:
            dropped.remove(spec)

    return dropped
