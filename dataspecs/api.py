__all__ = ["from_dataclass", "from_typehint"]


# standard library
from collections.abc import Callable
from dataclasses import MISSING, fields, is_dataclass
from pathlib import PurePosixPath as Path
from typing import Any, TypeVar, Union, overload


# dependencies
from .specs import ROOT, ID, Data, Name, Spec, Specs, Specifier, Tag, Type
from .typing import DataClass, StrPath, gen_annotations, gen_subtypes, get_annotated


# type hints
TAny = TypeVar("TAny")
TSpec = TypeVar("TSpec", bound=Spec[Any])


@overload
def from_dataclass(
    obj: DataClass,
    /,
    *,
    id: StrPath = ROOT,
    merge: bool = True,
) -> Specs[Spec[Any]]: ...


@overload
def from_dataclass(
    obj: DataClass,
    /,
    *,
    id: StrPath = ROOT,
    merge: bool = True,
    factory: Callable[..., TSpec],
) -> Specs[TSpec]: ...


def from_dataclass(
    obj: DataClass,
    /,
    *,
    id: StrPath = ROOT,
    merge: bool = True,
    factory: Callable[..., TSpec] = Spec,
) -> Specs[Any]:
    """Create dataspecs from given data class.

    Args:
        obj: Data class (class or instance) to be parsed.
        id: Parent ID of the dataspecs.
        merge: Whether to merge the dataspecs of the same ID
            into single dataspec at the end of the creation.
        factory: Class or function for creating each dataspec.
            It must have the same arguments of the ``Spec`` class.

    Returns:
        Dataspecs created from the data class.

    """
    specs = Specs[Any]()

    if Specifier.istype(obj):
        return specs

    for field in fields(obj):
        specs.extend(
            from_typehint(
                field.type,
                data=getattr(obj, field.name, field.default),
                id=Path(id) / field.name,
                factory=factory,
                merge=False,
            )
        )

    return specs.merge() if merge else specs


@overload
def from_typehint(
    obj: Any,
    /,
    *,
    data: Any = None,
    id: StrPath = ROOT,
    merge: bool = True,
) -> Specs[Spec[Any]]: ...


@overload
def from_typehint(
    obj: Any,
    /,
    *,
    data: Any = None,
    id: StrPath = ROOT,
    merge: bool = True,
    factory: Callable[..., TSpec],
) -> Specs[TSpec]: ...


def from_typehint(
    obj: Any,
    /,
    *,
    data: Any = None,
    id: StrPath = ROOT,
    merge: bool = True,
    factory: Callable[..., TSpec] = Spec,
) -> Specs[Any]:
    """Create dataspecs from given type hint.

    Args:
        obj: Type or type hint to be parsed.
        data: Parent data of the dataspecs.
        id: Parent ID of the dataspecs.
        merge: Whether to merge the dataspecs of the same ID
            into single dataspec at the end of the creation.
        factory: Class or function for creating each dataspec.
            It must have the same arguments of the ``Spec`` class.

    Returns:
        Dataspecs created from the type hint.

    """
    id = Path(id)
    specs = Specs[Any](
        [
            factory(
                data=find(obj, Data, data),
                id=(id := id.parent / find(obj, ID, id.name)),
                name=find(obj, Name, id.name),
                tags=find(obj, Tag),
                type=find(obj, Type, get_annotated(obj)),
            )
        ]
    )

    if Specifier.istype(data):
        return specs

    for n, sub in enumerate(gen_subtypes(obj)):
        specs.extend(
            from_typehint(
                sub,
                id=id / str(n),
                factory=factory,
                merge=False,
            )
        )

    for sub in gen_annotations(obj, filter=is_dataclass):
        specs.extend(
            from_dataclass(
                sub,
                id=id,
                factory=factory,
                merge=False,
            )
        )

    return specs.merge() if merge else specs


@overload
def find(
    obj: Any,
    of: type[Specifier[TAny]],
    /,
) -> frozenset[TAny]: ...


@overload
def find(
    obj: Any,
    of: type[Specifier[TAny]],
    default: Any,
    /,
) -> TAny: ...


def find(
    obj: Any,
    of: type[Specifier[TAny]],
    default: Any = MISSING,
    /,
) -> Union[frozenset[TAny], TAny]:
    """Find specifier(s) of given type and return value(s)."""
    anns = list(gen_annotations(obj, filter=of.istype))

    if default is MISSING:
        return frozenset(ann.value for ann in anns)

    if len(anns) == 0:
        return default

    if len(anns) == 1:
        return anns[0].value

    raise ValueError("Multiple items are not allowed with default.")
