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
    get_others,
    get_subtypes,
    get_tags,
)


@overload
def from_dataclass(
    obj: DataClass,
    /,
    *,
    parent_id: StrPath = ROOT,
) -> Specs[Spec[Any]]: ...


@overload
def from_dataclass(
    obj: DataClass,
    /,
    *,
    parent_id: StrPath = ROOT,
    spec_factory: Callable[..., TSpec],
) -> Specs[TSpec]: ...


def from_dataclass(
    obj: DataClass,
    /,
    *,
    parent_id: StrPath = ROOT,
    spec_factory: Any = Spec,
) -> Any:
    """Create data specs from a dataclass (object).

    Args:
        obj: Dataclass (object) to be parsed.
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
    parent_id: StrPath = ROOT,
    parent_data: Any = None,
) -> Specs[Spec[Any]]: ...


@overload
def from_typehint(
    obj: Any,
    /,
    *,
    parent_id: StrPath = ROOT,
    parent_data: Any = None,
    spec_factory: Callable[..., TSpec],
) -> Specs[TSpec]: ...


def from_typehint(
    obj: Any,
    /,
    *,
    parent_id: StrPath = ROOT,
    parent_data: Any = None,
    spec_factory: Any = Spec,
) -> Any:
    """Create data specs from a type hint.

    Args:
        obj: Type hint to be parsed.
        parent_id: ID of the parent data spec.
        parent_data: Data of the parent data spec.
        spec_factory: Factory for creating each data spec.

    Returns:
        Data specs created from the type hint.

    """
    specs: Specs[Any] = Specs()

    specs.append(
        spec_factory(
            id=ID(parent_id),
            tags=get_tags(first := get_first(obj)),
            type=get_annotated(first, recursive=True),
            data=parent_data,
            meta=get_others(first),
        )
    )

    for index, subtype in enumerate(get_subtypes(first)):
        specs.extend(
            from_typehint(
                subtype,
                parent_id=ID(parent_id) / str(index),
                spec_factory=spec_factory,
            )
        )

    for dc in get_dataclasses(first):
        specs.extend(
            from_dataclass(
                dc,
                parent_id=ID(parent_id),
                spec_factory=spec_factory,
            )
        )

    return specs
