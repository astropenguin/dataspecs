__all__ = ["DataClass", "Tag"]


# standard library
import types
from dataclasses import Field, is_dataclass
from enum import Enum
from typing import Annotated, Any, ClassVar, Literal, Protocol, Union


# dependencies
from typing_extensions import get_args, get_origin


class DataClass(Protocol):
    """Type hint for any dataclass object."""

    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]


class Tag(str, Enum):
    """Base string enum for specification tags."""

    @staticmethod
    def _generate_next_value_(
        name: str,
        start: int,
        count: int,
        last_values: list[str],
    ) -> str:
        """Return the lowercase string of the member name."""
        return name.lower()


def is_annotated(tp: Any) -> bool:
    """Check if a type is annotated."""
    return get_origin(tp) is Annotated


def is_literal(tp: Any) -> bool:
    """Check if a type is a literal type."""
    return get_origin(tp) is Literal


def is_union(tp: Any) -> bool:
    """Check if a type is a union of types."""
    if UnionType := getattr(types, "UnionType", None):
        return get_origin(tp) is Union or isinstance(tp, UnionType)
    else:
        return get_origin(tp) is Union


def get_annotated(tp: Any) -> Any:
    """Return annotated type of a type if it exists."""
    return get_args(tp)[0] if is_annotated(tp) else tp


def get_annotations(tp: Any) -> list[Any]:
    """Return annotations of a type if they exist."""
    return list(get_args(tp))[1:] if is_annotated(tp) else []


def get_dataclasses(tp: Any) -> list[DataClass]:
    """Return dataclass objects that annotate a type."""
    return [ann for ann in get_annotations(tp) if is_dataclass(ann)]


def get_first(tp: Any) -> Any:
    """Return the first type if a type is a union of types."""
    return get_args(tp)[0] if is_union(tp) else tp


def get_literals(tp: Any) -> list[Any]:
    """Return literals if a type is a literal type."""
    return list(get_args(tp)) if is_literal(tp) else []


def get_subscriptions(tp: Any) -> list[Any]:
    """Return subscriptions of a type if they exist."""
    return list(get_args(get_annotated(tp)))


def get_tags(tp: Any) -> list[Tag]:
    """Return tags that annotate a type."""
    return [ann for ann in get_annotations(tp) if isinstance(ann, Tag)]
