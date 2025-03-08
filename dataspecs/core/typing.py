# standard library
import types
from dataclasses import Field
from typing import Annotated, Any, ClassVar, Iterator, Literal, Protocol, Union
from typing import _strip_annotations  # type: ignore


# dependencies
from typing_extensions import get_args, get_origin


# type hints
class DataClassInstance(Protocol):
    """Type hint for any data-class instance."""

    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]


DataClass = Union[DataClassInstance, type[DataClassInstance]]
"""Type hint for any data class or data-class instance."""


def gen_annotations(obj: Any, /) -> Iterator[Any]:
    """Generate annotations if given object is an annotated type."""
    if is_annotated(obj):
        annotated, *annotations = get_args(obj)
        yield from gen_annotations(annotated)
        yield from annotations
    elif is_union(obj):
        for arg in get_args(obj):
            yield from gen_annotations(arg)


def gen_subtypes(obj: Any, /) -> Iterator[Any]:
    """Generate subtypes if given object is a generic type."""
    if is_annotated(obj):
        yield from gen_subtypes(get_args(obj)[0])
    elif is_union(obj):
        for arg in get_args(obj):
            yield from gen_subtypes(arg)
    else:
        for arg in get_args(obj):
            if not (is_ellipsis(arg) or is_literal(arg)):
                yield arg


def get_annotated(obj: Any, /) -> Any:
    """Return the bare type if given object is an annotated type."""
    return _strip_annotations(obj)  # type: ignore


def is_annotated(obj: Any, /) -> bool:
    """Check if given object is an annotated type."""
    return get_origin(obj) is Annotated


def is_ellipsis(obj: Any, /) -> bool:
    """Check if given object is an ellipsis."""
    return obj is Ellipsis


def is_literal(obj: Any, /) -> bool:
    """Check if given object is a literal type."""
    return get_origin(obj) is Literal


def is_union(obj: Any, /) -> bool:
    """Check if given object is a union type."""
    if (UnionType := getattr(types, "UnionType", None)) is not None:
        # For Python >= 3.10
        return get_origin(obj) is Union or isinstance(obj, UnionType)
    else:
        # For Python < 3.10
        return get_origin(obj) is Union
