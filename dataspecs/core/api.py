__all__ = ["from_dataclass", "from_typehint"]


# standard library
from dataclasses import MISSING, fields
from typing import Any, Callable, Optional, overload


# dependencies
from .specs import ID, ROOT, Spec, Specs, TSpec
from .typing import (
    DataClass,
    StrPath,
    get_annotated,
    get_annotations,
    get_dataclasses,
    get_first,
    get_subtypes,
    get_tags,
)


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
    factory: Callable[..., TSpec],
    id: StrPath = ROOT,
) -> Specs[TSpec]: ...


def from_dataclass(
    obj: DataClass,
    /,
    *,
    factory: Any = Spec,
    id: StrPath = ROOT,
) -> Any:
    """Create data specs from a dataclass (object).

    Args:
        obj: Dataclass (object) to be parsed.
        factory: Factory for creating each data spec.
        id: ID of the parent data spec.

    Returns:
        Data specs created from the dataclass (object).

    Examples:
        ::

            from enum import auto
            from dataclasses import dataclass
            from dataspecs import TagBase, from_dataclass
            from typing import Annotated as Ann

            class Tag(TagBase):
                ATTR = auto()
                DATA = auto()
                DTYPE = auto()

            @dataclass
            class Weather:
                temp: Ann[list[Ann[float, Tag.DTYPE]], Tag.DATA]
                humid: Ann[list[Ann[float, Tag.DTYPE]], Tag.DATA]
                location: Ann[str, Tag.ATTR]

            from_dataclass(Weather([20.0, 25.0], [50.0, 55.0], "Tokyo"))

        ::

            Specs([
                Spec(
                    id=ID('/temp'),
                    tags=(<Tag.DATA: 2>,),
                    type=list[float],
                    data=[20.0, 25.0],
                ),
                Spec(
                    id=ID('/temp/0'),
                    tags=(<Tag.DTYPE: 3>,),
                    type=<class 'float'>,
                    data=None,
                ),
                Spec(
                    id=ID('/humid'),
                    tags=(<Tag.DATA: 2>,),
                    type=list[float],
                    data=[50.0, 55.0],
                ),
                Spec(
                    id=ID('/humid/0'),
                    tags=(<Tag.DTYPE: 3>,),
                    type=<class 'float'>,
                    data=None,
                ),
                Spec(
                    id=ID('/location'),
                    tags=(<Tag.ATTR: 1>,),
                    type=<class 'str'>,
                    data='Tokyo',
                ),
            ])

    """
    specs: Specs[Any] = Specs()

    for field in fields(obj):
        specs.extend(
            from_typehint(
                field.type,
                factory=factory,
                id=ID(id) / field.name,
                data=getattr(obj, field.name, field.default),
                metadata=dict(field.metadata),
                origin=obj,
            )
        )

    return specs


@overload
def from_typehint(
    obj: Any,
    /,
    *,
    id: StrPath = ROOT,
    data: Any = MISSING,
    metadata: Optional[dict[str, Any]] = None,
    origin: Optional[Any] = None,
) -> Specs[Spec[Any]]: ...


@overload
def from_typehint(
    obj: Any,
    /,
    *,
    factory: Callable[..., TSpec],
    id: StrPath = ROOT,
    data: Any = MISSING,
    metadata: Optional[dict[str, Any]] = None,
    origin: Optional[Any] = None,
) -> Specs[TSpec]: ...


def from_typehint(
    obj: Any,
    /,
    *,
    factory: Any = Spec,
    id: StrPath = ROOT,
    data: Any = None,
    metadata: Optional[dict[str, Any]] = None,
    origin: Optional[Any] = None,
) -> Any:
    """Create data specs from a type hint.

    Args:
        obj: Type hint to be parsed.
        factory: Factory for creating each data spec.
        id: ID of the parent data spec.
        data: Data of the parent data spec.
        metadata: Metadata of the parent data spec.

    Returns:
        Data specs created from the type hint.

    Examples:
        ::

            from enum import auto
            from dataspecs import TagBase, from_typehint
            from typing import Annotated as Ann

            class Tag(TagBase):
                DATA = auto()
                DTYPE = auto()

            from_typehint(Ann[list[Ann[float, Tag.DTYPE]], Tag.DATA])

        ::

            Specs([
                Spec(
                    id=ID('/'),
                    tags=(<Tag.DATA: 1>,),
                    type=list[float],
                    data=None,
                ),
                Spec(
                    id=ID('/0'),
                    tags=(<Tag.DTYPE: 2>,),
                    type=<class 'float'>,
                    data=None,
                ),
            ])

    """
    specs: Specs[Any] = Specs()

    specs.append(
        factory(
            id=ID(id),
            tags=get_tags(first := get_first(obj)),
            type=get_annotated(first, recursive=True),
            data=data,
            annotations=get_annotations(first),
            metadata={} if metadata is None else dict(metadata),
            origin=origin,
        )
    )

    for index, subtype in enumerate(get_subtypes(first)):
        specs.extend(
            from_typehint(
                subtype,
                factory=factory,
                id=ID(id) / str(index),
                origin=obj,
            )
        )

    for sub_dataclass in get_dataclasses(first):
        specs.extend(
            from_dataclass(
                sub_dataclass,
                factory=factory,
                id=ID(id),
            )
        )

    return specs
