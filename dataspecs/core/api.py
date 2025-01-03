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
    get_meta,
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
    spec_factory: Callable[..., TSpec],
) -> Specs[TSpec]: ...


def from_dataclass(
    obj: DataClass,
    /,
    *,
    id: StrPath = ROOT,
    spec_factory: Any = Spec,
) -> Any:
    """Create data specs from a dataclass (object).

    Args:
        obj: Dataclass (object) to be parsed.
        id: ID of the parent data spec.
        spec_factory: Factory for creating each data spec.

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

    # 1. data spec of the dataclass (object) itself
    specs.append(
        spec_factory(
            id=ID(id),
            tags=(),
            type=type(obj),
            data=obj,
        )
    )

    # 2. data specs of the dataclass fields
    for field in fields(obj):
        specs.extend(
            from_typehint(
                field.type,
                id=ID(id) / field.name,
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
    id: StrPath = ROOT,
    parent_data: Any = None,
) -> Specs[Spec[Any]]: ...


@overload
def from_typehint(
    obj: Any,
    /,
    *,
    id: StrPath = ROOT,
    parent_data: Any = None,
    spec_factory: Callable[..., TSpec],
) -> Specs[TSpec]: ...


def from_typehint(
    obj: Any,
    /,
    *,
    id: StrPath = ROOT,
    parent_data: Any = None,
    spec_factory: Any = Spec,
) -> Any:
    """Create data specs from a type hint.

    Args:
        obj: Type hint to be parsed.
        id: ID of the parent data spec.
        parent_data: Data of the parent data spec.
        spec_factory: Factory for creating each data spec.

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

    # 1. data spec of the type hint itself
    specs.append(
        spec_factory(
            id=ID(id),
            tags=get_tags(first := get_first(obj)),
            type=get_annotated(first, recursive=True),
            data=parent_data,
            meta=get_meta(first),
        )
    )

    # 2. data specs of the type hint subtypes
    for name, subtype in enumerate(get_subtypes(first)):
        specs.extend(
            from_typehint(
                subtype,
                id=ID(id) / str(name),
                spec_factory=spec_factory,
            )
        )

    # 3. data specs of the sub-dataclasses (objects)
    for name, dataclass in named_enumerate(get_dataclasses(first)):
        specs.extend(
            from_dataclass(
                dataclass,
                id=ID(id) / str(name),
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
