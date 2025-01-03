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
    id: StrPath = ROOT,
    factory: Callable[..., TSpec],
) -> Specs[TSpec]: ...


def from_dataclass(
    obj: DataClass,
    /,
    *,
    id: StrPath = ROOT,
    factory: Any = Spec,
) -> Any:
    """Create data specs from a dataclass (object).

    Args:
        obj: Dataclass (object) to be parsed.
        id: ID of the parent data spec.
        factory: Factory for creating each data spec.

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
                    id=ID('/'),
                    tags=(),
                    type=<class '__main__.Weather'>,
                    data=Weather(temp=[20.0, 25.0], humid=[50.0, 55.0], location='Tokyo'),
                ),
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
                id=ID(id) / field.name,
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
    id: StrPath = ROOT,
    data: Any = None,
) -> Specs[Spec[Any]]: ...


@overload
def from_typehint(
    obj: Any,
    /,
    *,
    id: StrPath = ROOT,
    data: Any = None,
    factory: Callable[..., TSpec],
) -> Specs[TSpec]: ...


def from_typehint(
    obj: Any,
    /,
    *,
    id: StrPath = ROOT,
    data: Any = None,
    factory: Any = Spec,
) -> Any:
    """Create data specs from a type hint.

    Args:
        obj: Type hint to be parsed.
        id: ID of the parent data spec.
        data: Data of the parent data spec.
        factory: Factory for creating each data spec.

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
        )
    )

    for index, subtype in enumerate(get_subtypes(first)):
        specs.extend(
            from_typehint(
                subtype,
                id=ID(id) / str(index),
                factory=factory,
            )
        )

    for dataclass in get_dataclasses(first):
        specs.extend(
            from_dataclass(
                dataclass,
                id=ID(id),
                factory=factory,
            )
        )

    return specs
