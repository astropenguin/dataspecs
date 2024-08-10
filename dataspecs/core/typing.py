__all__ = ["TagBase"]


# standard library
import types
from dataclasses import Field, is_dataclass
from enum import Enum
from os import PathLike
from typing import Annotated, Any, ClassVar, Literal, Protocol, Union


# dependencies
from typing_extensions import TypeGuard, get_args, get_origin


# type hints
StrPath = Union[str, PathLike[str]]


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


def get_annotated(obj: Any, /, recursive: bool = False) -> Any:
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
    """Return dataclasses (objects) that annotate a type hint."""
    return tuple(filter(is_dataclass, get_annotations(obj)))


def get_first(obj: Any, /) -> Any:
    """Return the first type if a type hint is a union type."""
    return get_args(obj)[0] if is_union(obj) else obj


def get_subtypes(obj: Any, /) -> tuple[Any, ...]:
    """Return subtypes of a type hint if they exist."""
    if is_literal(annotated := get_annotated(obj)):
        return ()

    return get_args(annotated)


def get_tags(obj: Any, /) -> tuple[TagBase, ...]:
    """Return tags that annotate a type hint."""
    return tuple(filter(is_tag, get_annotations(obj)))


def is_annotated(obj: Any, /) -> bool:
    """Check if a type hint is annotated."""
    return get_origin(obj) is Annotated


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
    if get_origin(obj) is Union:
        return True

    # Only for Python >= 3.10
    if UnionType := getattr(types, "UnionType", None):
        return isinstance(obj, UnionType)

    return False
