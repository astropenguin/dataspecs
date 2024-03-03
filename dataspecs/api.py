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
    get_subscriptions,
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
    tagged_only: bool = True,
) -> Specs[Spec]: ...


@overload
def from_dataclass(
    obj: DataClass,
    /,
    *,
    parent_id: StrPath = ROOT,
    tagged_only: bool = True,
    spec_factory: Callable[..., TSpec],
) -> Specs[TSpec]: ...


def from_dataclass(
    obj: DataClass,
    /,
    *,
    parent_id: StrPath = ROOT,
    tagged_only: bool = True,
    spec_factory: Any = Spec,
) -> Any:
    """Create data specs from a dataclass object.

    Args:
        obj: Dataclass object to be parsed.
        parent_id: ID of the parent data spec.
        tagged_only: Whether to add only tagged data specs.
        spec_factory: Factory for creating each data spec.

    Returns:
        Data specs created from the dataclass object.

    """
    specs: Specs[Any] = Specs()

    for field in fields(obj):
        if not (tags := get_tags(field.type)) and tagged_only:
            continue

        specs.append(
            spec_factory(
                id=(child_id := ID(parent_id) / field.name),
                tags=tags,
                data=getattr(obj, field.name, field.default),
                type=field.type,
                origin=obj,
            )
        )
        specs.extend(
            from_typehint(
                field.type,
                parent_id=child_id,
                tagged_only=tagged_only,
                spec_factory=spec_factory,
            )
        )

    return specs


@overload
def from_typehint(
    obj: Any,
    /,
    *,
    parent_id: StrPath = ROOT,
    tagged_only: bool = True,
) -> Specs[Spec]: ...


@overload
def from_typehint(
    obj: Any,
    /,
    *,
    parent_id: StrPath = ROOT,
    tagged_only: bool = True,
    spec_factory: Callable[..., TSpec],
) -> Specs[TSpec]: ...


def from_typehint(
    obj: Any,
    /,
    *,
    parent_id: StrPath = ROOT,
    tagged_only: bool = True,
    spec_factory: Any = Spec,
) -> Any:
    """Create data specs from a type hint.

    Args:
        obj: Type hint to be parsed.
        parent_id: ID of the parent data spec.
        tagged_only: Whether to add only tagged data specs.
        spec_factory: Factory for creating each data spec.

    Returns:
        Data specs created from the type hint.

    """
    specs: Specs[Any] = Specs()

    for name, type_ in enumerate(get_subscriptions(obj)):
        if not (tags := get_tags(type_)) and tagged_only:
            continue

        specs.append(
            spec_factory(
                id=(child_id := ID(parent_id) / str(name)),
                tags=tags,
                data=get_annotated(type_),
                origin=obj,
            )
        )
        specs.extend(
            from_typehint(
                type_,
                parent_id=child_id,
                tagged_only=tagged_only,
                spec_factory=spec_factory,
            )
        )

    for dataclass in get_dataclasses(obj):
        specs.extend(
            from_dataclass(
                dataclass,
                parent_id=parent_id,
                tagged_only=tagged_only,
                spec_factory=spec_factory,
            )
        )

    return specs
