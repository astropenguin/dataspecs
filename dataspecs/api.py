__all__ = ["from_dataclass", "from_typehint"]


# standard library
from dataclasses import fields
from typing import Any, Callable, TypeVar, overload


# dependencies
from .specs import ID, ROOT, Spec, Specs
from .typing import (
    DataClass,
    StrPath,
    get_annotated,
    get_dataclasses,
    get_first,
    get_subtypes,
    get_tags,
)


# type hints
TSpec = TypeVar("TSpec", bound=Spec)


@overload
def from_dataclass(
    obj: DataClass,
    /,
    *,
    parent_id: StrPath = ROOT,
    first_only: bool = True,
    tagged_only: bool = True,
) -> Specs[Spec]: ...


@overload
def from_dataclass(
    obj: DataClass,
    /,
    *,
    parent_id: StrPath = ROOT,
    first_only: bool = True,
    tagged_only: bool = True,
    spec_factory: Callable[..., TSpec],
) -> Specs[TSpec]: ...


def from_dataclass(
    obj: DataClass,
    /,
    *,
    parent_id: StrPath = ROOT,
    first_only: bool = True,
    tagged_only: bool = True,
    spec_factory: Any = Spec,
) -> Any:
    """Create data specs from a dataclass object.

    Args:
        obj: Dataclass object to be parsed.
        parent_id: ID of the parent data spec.
        first_only: If ``True`` and a type hint is a union of types,
            parse the first type only instead of the whole type hint.
        tagged_only: If ``True``, drop leaf (i.e. terminal) and
            adjacent superior data specs that do not have any tags.
        spec_factory: Factory for creating each data spec.

    Returns:
        Data specs created from the dataclass object.

    """
    specs: Specs[Any] = Specs()

    for field in fields(obj):
        reftype = get_first(field.type) if first_only else field.type

        specs.append(
            spec_factory(
                id=(child_id := ID(parent_id) / field.name),
                tags=get_tags(reftype),
                type=get_annotated(reftype),
                data=getattr(obj, field.name, field.default),
                origin=obj,
            )
        )
        specs.extend(
            from_typehint(
                reftype,
                parent_id=child_id,
                first_only=first_only,
                tagged_only=tagged_only,
                spec_factory=spec_factory,
            )
        )

    return drop_leaves(specs) if tagged_only else specs


@overload
def from_typehint(
    obj: Any,
    /,
    *,
    parent_id: StrPath = ROOT,
    first_only: bool = True,
    tagged_only: bool = True,
) -> Specs[Spec]: ...


@overload
def from_typehint(
    obj: Any,
    /,
    *,
    parent_id: StrPath = ROOT,
    first_only: bool = True,
    tagged_only: bool = True,
    spec_factory: Callable[..., TSpec],
) -> Specs[TSpec]: ...


def from_typehint(
    obj: Any,
    /,
    *,
    parent_id: StrPath = ROOT,
    first_only: bool = True,
    tagged_only: bool = True,
    spec_factory: Any = Spec,
) -> Any:
    """Create data specs from a type hint.

    Args:
        obj: Type hint to be parsed.
        parent_id: ID of the parent data spec.
        first_only: If ``True`` and a type hint is a union of types,
            parse the first type only instead of the whole type hint.
        tagged_only: If ``True``, drop leaf (i.e. terminal) and
            adjacent superior data specs that do not have any tags.
        spec_factory: Factory for creating each data spec.

    Returns:
        Data specs created from the type hint.

    """
    specs: Specs[Any] = Specs()
    reftype = get_first(obj) if first_only else obj

    for name, subtype in enumerate(get_subtypes(reftype)):
        specs.append(
            spec_factory(
                id=(child_id := ID(parent_id) / str(name)),
                tags=get_tags(subtype),
                type=get_annotated(subtype),
            )
        )
        specs.extend(
            from_typehint(
                subtype,
                parent_id=child_id,
                first_only=first_only,
                tagged_only=tagged_only,
                spec_factory=spec_factory,
            )
        )

    for dataclass in get_dataclasses(obj):
        specs.extend(
            from_dataclass(
                dataclass,
                parent_id=parent_id,
                first_only=first_only,
                tagged_only=tagged_only,
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
