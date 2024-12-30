__all__ = ["from_dataclass", "from_typehint"]


# standard library
from collections import Counter, defaultdict
from dataclasses import fields
from typing import Any, Callable, Iterable, Iterator, overload


# dependencies
from humps import decamelize
from .specs import ID, ROOT, Spec, Specs, TSpec
from .typing import (
    DataClass,
    StrPath,
    TAny,
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
    """Create data specs from a dataclass or its object.

    Args:
        obj: Dataclass or its object to be parsed.
        parent_id: ID of the parent data spec.
        spec_factory: Factory for creating each data spec.

    Returns:
        Data specs created from the dataclass or its object.

    """
    specs: Specs[Any] = Specs()

    # 1. data spec of the dataclass or its object itself
    specs.append(
        spec_factory(
            id=ID(parent_id),
            type=type(obj),
            data=obj,
        )
    )

    # 2. data specs of the dataclass fields
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

    # 1. data spec of the type hint itself
    specs.append(
        spec_factory(
            id=ID(parent_id),
            type=get_annotated(obj := get_first(obj), recursive=True),
            data=parent_data,
            tags=get_tags(obj),
            meta=get_others(obj),
        )
    )

    # 2. data specs of the type hint subtypes
    for name, subtype in enumerate(get_subtypes(obj)):
        specs.extend(
            from_typehint(
                subtype,
                parent_id=ID(parent_id) / str(name),
                spec_factory=spec_factory,
            )
        )

    # 3. data specs of the sub-dataclasses or their objects
    for name, dataclass in named_enumerate(get_dataclasses(obj)):
        specs.extend(
            from_dataclass(
                dataclass,
                parent_id=ID(parent_id) / str(name),
                spec_factory=spec_factory,
            )
        )

    return specs


def named_enumerate(iterable: Iterable[TAny], /) -> Iterator[tuple[str, TAny]]:
    """Same as enumerate but returns snake-case type names (with counts)."""
    counts = Counter(type(obj) for obj in iterable)
    indexes: defaultdict[type[Any], int] = defaultdict(int)

    for obj in iterable:
        if counts[(cls := type(obj))] == 1:
            yield decamelize(cls.__name__), obj
        else:
            yield f"{decamelize(cls.__name__)}_{indexes[cls]}", obj
            indexes[cls] += 1
