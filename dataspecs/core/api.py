__all__ = ["from_dataclass", "from_typehint"]


# standard library
from collections.abc import Callable, Iterator
from dataclasses import fields, is_dataclass
from os import PathLike
from pathlib import PurePosixPath as Path
from typing import Any, TypeVar, Union, overload


# dependencies
from typing_extensions import TypeGuard
from .spec import Attr, Spec, is_attr, is_data, is_id, is_name, is_tag, is_type, is_unit
from .specs import Specs
from .typing import DataClass, gen_annotations, gen_subtypes, get_annotated


# type hints
TAny = TypeVar("TAny")
TSpec = TypeVar("TSpec", bound=Spec[Any])
Factory = Callable[..., TSpec]
Filter = Callable[[Any], TypeGuard[Attr[TAny]]]
StrPath = Union[PathLike[str], str]


# constants
ROOT = "/"


@overload
def from_dataclass(
    obj: DataClass,
    /,
    *,
    id: StrPath = ROOT,
) -> Specs[Spec[Any]]: ...


@overload
def from_dataclass(
    obj: DataClass,
    /,
    *,
    id: StrPath = ROOT,
    factory: Factory[TSpec],
) -> Specs[TSpec]: ...


def from_dataclass(
    obj: DataClass,
    /,
    *,
    id: StrPath = ROOT,
    factory: Factory[TSpec] = Spec,
) -> Specs[Any]:
    """Create dataspecs from given data class.

    Args:
        obj: Data class (class or instance) to be parsed.
        id: Parent dataspec ID.
        factory: Class or function for creating each dataspec.
            It must have the same arguments as the Spec class.

    Returns:
        Dataspecs created from the data class.

    """
    id = Path(id)
    specs: Specs[Any] = Specs()

    if is_attr(obj):
        return specs

    for field in fields(obj):
        specs.extend(
            from_typehint(
                field.type,
                id=id / field.name,
                data=getattr(obj, field.name, field.default),
                factory=factory,
            )
        )

    return specs


@overload
def from_typehint(
    obj: Any,
    /,
    *,
    data: Any = None,
    id: StrPath = ROOT,
) -> Specs[Spec[Any]]: ...


@overload
def from_typehint(
    obj: Any,
    /,
    *,
    data: Any = None,
    factory: Factory[TSpec],
    id: StrPath = ROOT,
) -> Specs[TSpec]: ...


def from_typehint(
    obj: Any,
    /,
    *,
    data: Any = None,
    factory: Factory[TSpec] = Spec,
    id: StrPath = ROOT,
) -> Specs[Any]:
    """Create dataspecs from given type hint.

    Args:
        obj: Type or type hint to be parsed.
        data: Parent dataspec data.
        id: Parent dataspec ID.
        factory: Class or function for creating each dataspec.
            It must have the same arguments as the Spec class.

    Returns:
        Dataspecs created from the type hint.

    """
    id = Path(id)
    specs: Specs[Any] = Specs()

    if is_attr(data := single(obj, data, filter=is_data)):
        return specs

    specs.append(
        factory(
            data=data,
            id=str(id := id.parent / single(obj, id.name, filter=is_id)),
            name=single(obj, id.name, filter=is_name),
            tags=multiple(obj, filter=is_tag),
            type=single(obj, get_annotated(obj), filter=is_type),
            unit=single(obj, None, filter=is_unit),
        )
    )

    for n, sub in enumerate(gen_subtypes(obj)):
        specs.extend(from_typehint(sub, id=id / str(n), factory=factory))

    for sub in gen_annotations(obj, filter=is_dataclass):
        specs.extend(from_dataclass(sub, id=id, factory=factory))

    return specs


def gen_attrs(obj: Any, /, *, filter: Filter[TAny] = is_attr) -> Iterator[TAny]:
    """Generate dataspec attributes from given object."""
    if is_dataclass(obj):
        for name in obj.__annotations__:
            if filter(annotation := getattr(obj, name)):
                yield annotation.attr
    else:
        for annotation in gen_annotations(obj, filter=filter):
            yield annotation.attr

        for annotation in gen_annotations(obj, filter=is_dataclass):
            yield from gen_attrs(annotation, filter=filter)


def multiple(obj: Any, /, *, filter: Filter[TAny] = is_attr) -> frozenset[TAny]:
    """Return multiple dataspec attributes from given object."""
    return frozenset(gen_attrs(obj, filter=filter))


def single(obj: Any, default: Any, /, *, filter: Filter[TAny] = is_attr) -> TAny:
    """Return single dataspec attribute from given object."""
    if len(attrs := list(gen_attrs(obj, filter=filter))) >= 2:
        raise ValueError("Multiple dataspec attributes are not allowed.")
    else:
        return default if not attrs else attrs[0]
