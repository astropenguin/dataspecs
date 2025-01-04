__all__ = ["TagBase"]


# standard library
import types
from dataclasses import Field, is_dataclass
from enum import Enum
from os import PathLike
from typing import Annotated, Any, ClassVar, Literal, Protocol, TypeVar, Union


# dependencies
from typing_extensions import TypeGuard, get_args, get_origin


# type hints
StrPath = Union[str, PathLike[str]]
TAny = TypeVar("TAny")
UAny = TypeVar("UAny")


class DataClassObject(Protocol):
    """Type hint for any dataclass object."""

    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]


DataClass = Union[DataClassObject, type[DataClassObject]]
"""Type hint for any dataclass or dataclass object."""


class TagBase(Enum):
    """Base enum of tag for data specs.

    Since ``TagBase`` itself does not have any members,
    users should create their own tags by inheriting it::

        from enum import auto
        from dataspecs import TagBase

        class Tag(TagBase):
            ATTR = auto()
            DATA = auto()
            NAME = auto()

    """

    pass


def get_annotated(obj: Any, /, *, recursive: bool = False) -> Any:
    """Return annotated type of a type hint if it exists."""
    if recursive:
        from typing import _strip_annotations  # type: ignore

        return _strip_annotations(obj)  # type: ignore
    else:
        return get_args(obj)[0] if is_annotated(obj) else obj


def get_annotations(obj: Any, /) -> tuple[Any, ...]:
    """Return annotations of a type hint if they exist."""
    return get_args(obj)[1:] if is_annotated(obj) else ()


def get_dataclasses(obj: Any, /) -> tuple[DataClass, ...]:
    """Return annotations of dataclasses (objects)."""
    return tuple(filter(is_dataclass, get_annotations(obj)))


def get_first(obj: Any, /) -> Any:
    """Return the first type if a type hint is a union type."""
    if is_union(annotated := get_annotated(obj)):
        first = get_args(annotated)[0]
    else:
        first = annotated

    for annotation in get_annotations(obj):
        first = Annotated[first, annotation]

    return first


def get_subtypes(obj: Any, /) -> tuple[Any, ...]:
    """Return subtypes of a type hint if they exist."""
    if is_literal(annotated := get_annotated(obj)):
        return ()

    return get_args(annotated)


def get_tags(obj: Any, /) -> tuple[TagBase, ...]:
    """Return annotations of tags for data specs."""
    return tuple(filter(is_tag, get_annotations(obj)))


def is_annotated(obj: Any, /) -> bool:
    """Check if a type hint is annotated."""
    return get_origin(obj) is Annotated


def is_anytype(obj: Any, /) -> TypeGuard[type[Any]]:
    """Check if an object is an any type."""
    return isinstance(obj, type)


def is_literal(obj: Any, /) -> bool:
    """Check if a type hint is a literal type."""
    return get_origin(obj) is Literal


def is_strpath(obj: Any, /) -> TypeGuard[StrPath]:
    """Check if an object is a string or a string path."""
    return isinstance(obj, (str, PathLike))


def is_tag(obj: Any, /) -> TypeGuard[TagBase]:
    """Check if an object is a specification tag."""
    return isinstance(obj, TagBase)


def is_tagtype(obj: Any, /) -> TypeGuard[type[TagBase]]:
    """Check if an object is a specification tag type."""
    return isinstance(obj, type) and issubclass(obj, TagBase)


def is_union(obj: Any, /) -> bool:
    """Check if a type hint is a union type."""
    if (UnionType := getattr(types, "UnionType", None)) is not None:
        # For Python >= 3.10
        return get_origin(obj) is Union or isinstance(obj, UnionType)
    else:
        # For Python < 3.10
        return get_origin(obj) is Union
