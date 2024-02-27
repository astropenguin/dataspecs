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
    specs: list[Any] = []

    for f in fields(obj):
        if not (tags := get_tags(f.type)) and tagged_only:
            continue

        specs.append(
            spec_factory(
                id=(id := ID(parent_id) / f.name),
                type=(hint := get_annotated(f.type)),
                data=getattr(obj, f.name, f.default),
                tags=tags,
                origin=obj,
            )
        )
        specs.extend(
            from_typehint(
                hint,
                parent_id=id,
                tagged_only=tagged_only,
                spec_factory=spec_factory,
            )
        )

        for dc in get_dataclasses(f.type):
            specs.extend(
                from_dataclass(
                    dc,
                    parent_id=id,
                    tagged_only=tagged_only,
                    spec_factory=spec_factory,
                )
            )

    return Specs(specs)


@overload
def from_typehint(
    obj: DataClass,
    /,
    *,
    parent_id: StrPath = ROOT,
    tagged_only: bool = True,
) -> Specs[Spec]: ...


@overload
def from_typehint(
    obj: DataClass,
    /,
    *,
    parent_id: StrPath = ROOT,
    tagged_only: bool = True,
    spec_factory: Callable[..., TSpec],
) -> Specs[TSpec]: ...


def from_typehint(
    obj: DataClass,
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
    specs: list[Any] = []

    for name, type in enumerate(get_subscriptions(obj)):
        if not (tags := get_tags(type)) and tagged_only:
            continue

        specs.append(
            spec_factory(
                id=(id := ID(parent_id) / str(name)),
                type=Any,
                data=(hint := get_annotated(type)),
                tags=tags,
                origin=obj,
            )
        )
        specs.extend(
            from_typehint(
                hint,
                parent_id=id,
                tagged_only=tagged_only,
                spec_factory=spec_factory,
            )
        )

        for dc in get_dataclasses(type):
            specs.extend(
                from_dataclass(
                    dc,
                    parent_id=id,
                    tagged_only=tagged_only,
                    spec_factory=spec_factory,
                )
            )

    return Specs(specs)
