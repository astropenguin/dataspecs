__all__ = ["SpecType", "is_specclass"]


# standard library
from dataclasses import fields, is_dataclass
from enum import Enum
from itertools import chain
from typing import Annotated, Any, Iterable, Optional, get_args, get_origin


class SpecType(str, Enum):
    """Base string enum for spec types."""

    @classmethod
    def annotates(cls, hint: Any) -> bool:
        """Check if a type hint is annotated by any member."""
        if get_origin(hint) is not Annotated:
            return False

        _, *anns = get_args(hint)
        return any(isinstance(ann, cls) for ann in anns)

    @staticmethod
    def _generate_next_value_(
        name: str,
        start: int,
        count: int,
        last_values: list[str],
    ) -> str:
        """Return the lowercase string of the member name."""
        return name.lower()


def is_specclass(obj: Any) -> bool:
    """Check if an object is a spec class or its instance."""
    if not is_dataclass(obj):
        return False

    return any(has_spechint(f.type) for f in fields(obj))


def get_spechint(hint: Any) -> Optional[Any]:
    """Get the first spec hint in a type hint if it exists."""
    for tp in walk(hint):
        if SpecType.annotates(tp):
            return tp


def has_spechint(hint: Any) -> bool:
    """Check if a type hint contains any spec hint."""
    return get_spechint(hint) is not None


def walk(hint: Any, *, self: bool = True) -> Iterable[Any]:
    """Walk through a type hint to generate all types."""
    if self:
        yield hint

    if get_origin(hint) is Annotated:
        yield from walk(get_args(hint)[0], self=False)
    else:
        yield from chain(*map(walk, get_args(hint)))
