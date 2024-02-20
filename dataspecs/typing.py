__all__ = ["DataClass", "TagBase"]


# standard library
from dataclasses import Field, is_dataclass
from enum import Enum
from typing import Annotated, Any, ClassVar, Literal, Protocol, Union


# dependencies
from typing_extensions import TypeGuard, get_args, get_origin


class DataClass(Protocol):
    """Type hint for any dataclass object."""

    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]


class TagBase(Enum):
    """Base enum for specification tags."""


def get_annotated(hint: Any) -> Any:
    """Return annotated type of a type hint if it exists."""
    return get_args(hint)[0] if is_annotated(hint) else hint


def get_annotations(hint: Any) -> tuple[Any, ...]:
    """Return annotations of a type hint if they exist."""
    return get_args(hint)[1:] if is_annotated(hint) else ()


def get_dataclasses(hint: Any) -> tuple[DataClass, ...]:
    """Return dataclass objects that annotate a type hint."""
    return tuple(filter(is_dataclass, get_annotations(hint)))


def get_first(hint: Any) -> Any:
    """Return the first type if a type hint is a union type."""
    return get_args(hint)[0] if is_union(hint) else hint


def get_literals(hint: Any) -> Any:
    """Return literals if a type hint is a literal type."""
    return get_args(hint) if is_literal(hint) else hint


def get_subscriptions(hint: Any) -> tuple[Any, ...]:
    """Return subscriptions of a type hint if they exist."""
    return get_args(get_annotated(hint))


def get_tags(hint: Any) -> tuple[TagBase, ...]:
    """Return tags that annotate a type hint."""
    return tuple(filter(is_tag, get_annotations(hint)))


def is_annotated(hint: Any) -> bool:
    """Check if a type hint is annotated."""
    return get_origin(hint) is Annotated


def is_literal(hint: Any) -> bool:
    """Check if a type hint is a literal type."""
    return get_origin(hint) is Literal


def is_tag(obj: Any) -> TypeGuard[TagBase]:
    """Check if an object is a specification tag."""
    return isinstance(obj, TagBase)


def is_union(hint: Any) -> bool:
    """Check if a type hint is a union type."""
    return get_origin(Union[hint]) is Union  # type: ignore