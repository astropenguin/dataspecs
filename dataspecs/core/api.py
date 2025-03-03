__all__ = ["from_dataclass", "from_typehint"]


# standard library
from collections.abc import Hashable, Iterator
from dataclasses import fields
from pathlib import PurePosixPath as Path
from typing import Any, Optional, overload


# dependencies
from .spec import (
    Spec,
    SpecFactory,
    TSpec,
    is_id,
    is_name,
    is_tag,
    is_tags,
    is_type,
    is_unit,
    is_value,
)
from .specs import Specs
from .typing import (
    DataClass,
    get_annotated,
    get_annotations,
    get_dataclasses,
    get_first,
    get_subtypes,
)


# constants
ROOT = "/"


@overload
def from_dataclass(
    obj: DataClass,
    /,
    *,
    id: str = ROOT,
) -> Specs[Spec[Any]]: ...


@overload
def from_dataclass(
    obj: DataClass,
    /,
    *,
    id: str = ROOT,
    factory: SpecFactory[TSpec],
) -> Specs[TSpec]: ...


def from_dataclass(
    obj: DataClass,
    /,
    *,
    id: str = ROOT,
    factory: SpecFactory[TSpec] = Spec,
) -> Specs[Any]:
    """Create data specs from given data class.

    Args:
        obj: Data class (class or instance) to be parsed.
        id: Parent data spec ID.
        factory: Class or function for creating each data spec.
            It must have the same arguments as the Spec class.

    Returns:
        Data specs created from the data class.

    """
    specs: Specs[Any] = Specs()

    for field in fields(obj):
        specs.extend(
            from_typehint(
                field.type,
                id=str(Path(id) / field.name),
                value=getattr(obj, field.name, field.default),
                factory=factory,
            )
        )

    return specs


@overload
def from_typehint(
    obj: Any,
    /,
    *,
    id: str = ROOT,
    value: Any = None,
) -> Specs[Spec[Any]]: ...


@overload
def from_typehint(
    obj: Any,
    /,
    *,
    id: str = ROOT,
    value: Any = None,
    factory: SpecFactory[TSpec],
) -> Specs[TSpec]: ...


def from_typehint(
    obj: Any,
    /,
    *,
    id: str = ROOT,
    value: Any = None,
    factory: SpecFactory[TSpec] = Spec,
) -> Specs[Any]:
    """Create data specs from given type hint.

    Args:
        obj: Type or type hint to be parsed.
        id: Parent data spec ID.
        value: Parent data spec value.
        factory: Class or function for creating each data spec.
            It must have the same arguments as the Spec class.

    Returns:
        Data specs created from the type hint.

    """
    first = get_first(obj)
    path = Path(id).parent / get_id(first, Path(id).name)

    specs = Specs(
        [
            factory(
                id=str(path),
                name=get_name(first, path.name),
                tags=set(get_tags(first)),
                type=get_type(first, get_annotated(first, recursive=True)),
                unit=get_unit(first),
                value=get_value(first, value),
            )
        ]
    )

    for n, sub in enumerate(get_subtypes(first)):
        specs.extend(from_typehint(sub, id=str(path / str(n)), factory=factory))

    for sub in get_dataclasses(first):
        specs.extend(from_dataclass(sub, id=str(path), factory=factory))

    return specs


def get_id(obj: Any, default: str, /) -> str:
    """Return the last-annotated ID from given type hint."""
    for id in filter(is_id, reversed(get_annotations(obj))):
        return id.wrapped

    return default


def get_name(obj: Any, default: Hashable, /) -> Hashable:
    """Return the last-annotated name from given type hint."""
    for name in filter(is_name, reversed(get_annotations(obj))):
        return name.wrapped

    return default


def get_tags(obj: Any, /) -> Iterator[str]:
    """Return all annotated tags from given type hint."""
    for tags in filter(is_tags, get_annotations(obj)):
        yield from tags.wrapped

    for tag in filter(is_tag, get_annotations(obj)):
        yield tag.wrapped

    for dataclass in get_dataclasses(obj):
        if (tags := getattr(dataclass, "tags", None)) is not None:
            yield from tags

        if (tag := getattr(dataclass, "tag", None)) is not None:
            yield tag


def get_type(obj: Any, default: type[Any], /) -> type[Any]:
    """Return the last-annotated type from given type hint."""
    for type in filter(is_type, reversed(get_annotations(obj))):
        return type.wrapped

    return default


def get_unit(obj: Any, /) -> Optional[str]:
    """Return the last-annotated unit from given type hint."""
    for unit in filter(is_unit, reversed(get_annotations(obj))):
        return unit.wrapped


def get_value(obj: Any, default: Optional[Any], /) -> Optional[Any]:
    """Return the last-annotated value from given type hint."""
    for value in filter(is_value, reversed(get_annotations(obj))):
        return value.wrapped

    return default
