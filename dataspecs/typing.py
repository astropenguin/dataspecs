__all__ = ["Use", "is_specclass"]


# standard library
from dataclasses import fields, is_dataclass
from enum import Enum
from itertools import chain
from typing import Annotated, Any, Iterable, Optional, get_args, get_origin


class Use(str, Enum):
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

    return any(has_spectype(f.type) for f in fields(obj))


def get_spectype(hint: Any) -> Optional[Any]:
    """Get the first spec type in a type hint if it exists."""
    for tp in walk(hint):
        if Use.annotates(tp):
            return tp


def has_spectype(hint: Any) -> bool:
    """Check if a type hint contains any spec type."""
    return get_spectype(hint) is not None


def walk(hint: Any, *, self: bool = True) -> Iterable[Any]:
    """Walk through a type hint to generate all types."""
    if self:
        yield hint

    if get_origin(hint) is Annotated:
        yield from walk(get_args(hint)[0], self=False)
    else:
        yield from chain(*map(walk, get_args(hint)))
