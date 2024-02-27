__all__ = ["TagBase"]


# standard library
from dataclasses import Field, is_dataclass
from enum import Enum
from os import PathLike
from typing import Annotated, Any, ClassVar, Protocol, Union


# dependencies
from typing_extensions import TypeGuard, get_args, get_origin


# type hints
StrPath = Union[str, PathLike[str]]


class DataClass(Protocol):
    """Type hint for any dataclass object."""

    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]


class TagBase(Enum):
    """Base enum of tag for data specs.

    Since ``TagBase`` itself cannot have any members,
    users should create their own tags by inheriting it::

        from enum import auto
        from dataspecs import TagBase

        class Tag(TagBase):
            ATTR = auto()
            DATA = auto()
            NAME = auto()

    """

    pass


def get_annotated(hint: Any, /) -> Any:
    """Return annotated type of a type hint if it exists."""
    return get_args(hint)[0] if is_annotated(hint) else hint


def get_annotations(hint: Any, /) -> tuple[Any, ...]:
    """Return annotations of a type hint if they exist."""
    return get_args(hint)[1:] if is_annotated(hint) else ()


def get_dataclasses(hint: Any, /) -> tuple[DataClass, ...]:
    """Return dataclass objects that annotate a type hint."""
    return tuple(filter(is_dataclass, get_annotations(hint)))


def get_subscriptions(hint: Any, /) -> tuple[Any, ...]:
    """Return subscriptions of a type hint if they exist."""
    return get_args(get_annotated(hint))


def get_tags(hint: Any, /) -> tuple[TagBase, ...]:
    """Return tags that annotate a type hint."""
    return tuple(filter(is_tag, get_annotations(hint)))


def is_annotated(hint: Any, /) -> bool:
    """Check if a type hint is annotated."""
    return get_origin(hint) is Annotated


def is_strpath(obj: Any, /) -> TypeGuard[StrPath]:
    """Check if an object is a string or a string path."""
    return isinstance(obj, (str, PathLike))


def is_tag(obj: Any, /) -> TypeGuard[TagBase]:
    """Check if an object is a specification tag."""
    return isinstance(obj, TagBase)
