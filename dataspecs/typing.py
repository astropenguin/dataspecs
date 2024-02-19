__all__ = ["DataClass", "Tag"]


# standard library
from dataclasses import Field
from enum import Enum
from typing import Any, ClassVar, Protocol


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
