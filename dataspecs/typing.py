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


def is_annotated(tp: Any) -> bool:
    """Check if a type is annotated."""
    return get_origin(tp) is Annotated


def is_literal(tp: Any) -> bool:
    """Check if a type is a literal type."""
    return get_origin(tp) is Literal


def is_tag(obj: Any) -> TypeGuard[TagBase]:
    """Check if an object is a specification tag."""
    return isinstance(obj, TagBase)


def is_union(tp: Any) -> bool:
    """Check if a type is a union type."""
    return get_origin(Union[tp]) is Union  # type: ignore


def get_annotated(tp: Any) -> Any:
    """Return annotated type of a type if it exists."""
    return get_args(tp)[0] if is_annotated(tp) else tp


def get_annotations(tp: Any) -> tuple[Any, ...]:
    """Return annotations of a type if they exist."""
    return get_args(tp)[1:] if is_annotated(tp) else ()


def get_dataclasses(tp: Any) -> tuple[DataClass, ...]:
    """Return dataclass objects that annotate a type."""
    return tuple(filter(is_dataclass, get_annotations(tp)))


def get_first(tp: Any) -> Any:
    """Return the first type if a type is a union of types."""
    return get_args(tp)[0] if is_union(tp) else tp


def get_literals(tp: Any) -> Any:
    """Return literals if a type is a literal type."""
    return get_args(tp) if is_literal(tp) else tp


def get_subscriptions(tp: Any) -> tuple[Any, ...]:
    """Return subscriptions of a type if they exist."""
    return get_args(get_annotated(tp))


def get_tags(tp: Any) -> tuple[TagBase, ...]:
    """Return tags that annotate a type."""
    return tuple(filter(is_tag, get_annotations(tp)))
