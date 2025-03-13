__all__ = ["from_dataclass", "from_typehint"]


# standard library
from collections.abc import Callable, Iterable, Iterator
from dataclasses import fields, is_dataclass
from pathlib import PurePosixPath as Path
from typing import Any, TypeVar, overload


# dependencies
from typing_extensions import TypeGuard
from .spec import (
    Attr,
    Spec,
    is_id,
    is_name,
    is_tag,
    is_tags,
    is_type,
    is_unit,
    is_value,
)
from .specs import Specs
from .typing import DataClass, gen_annotations, gen_subtypes, get_annotated


# type hints
TAny = TypeVar("TAny")
TSpec = TypeVar("TSpec", bound=Spec[Any])
Factory = Callable[..., TSpec]


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
    factory: Factory[TSpec],
) -> Specs[TSpec]: ...


def from_dataclass(
    obj: DataClass,
    /,
    *,
    id: str = ROOT,
    factory: Factory[TSpec] = Spec,
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
    factory: Factory[TSpec],
) -> Specs[TSpec]: ...


def from_typehint(
    obj: Any,
    /,
    *,
    id: str = ROOT,
    value: Any = None,
    factory: Factory[TSpec] = Spec,
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
    annotated = get_annotated(obj)
    annotations = list(gen_annotations(obj))
    path = Path(id).parent / get_attr(annotations, is_id, Path(id).name)

    specs = [
        factory(
            id=str(path),
            name=get_attr(annotations, is_name, path.name),
            tags=set(get_tags(annotations)),
            type=get_attr(annotations, is_type, annotated),
            unit=get_attr(annotations, is_unit, None),
            value=get_attr(annotations, is_value, value),
        )
    ]

    for n, sub in enumerate(gen_subtypes(obj)):
        specs.extend(from_typehint(sub, id=str(path / str(n)), factory=factory))

    for sub in filter(is_dataclass, annotations):
        specs.extend(from_dataclass(sub, id=str(path), factory=factory))

    return Specs(specs)


def get_attr(
    annotations: Iterable[Any],
    selector: Callable[..., TypeGuard[Attr[TAny]]],
    default: Any,
    /,
) -> TAny:
    """Return a data-spec attribute from given annotations."""
    if not (attrs := list(filter(selector, annotations))):
        return default

    if len(attrs) == 1:
        return attrs[0].wrapped

    raise ValueError("Multiple attributes are not allowed.")


def get_tags(annotations: Iterable[Any], /) -> Iterator[str]:
    """Return data-spec tags from given annotations."""
    for tags in filter(is_tags, annotations):
        yield from tags.wrapped

    for tag in filter(is_tag, annotations):
        yield tag.wrapped

    for sub in filter(is_dataclass, annotations):
        if (tags := getattr(sub, "tags", None)) is not None:
            yield from tags

        if (tag := getattr(sub, "tag", None)) is not None:
            yield tag
