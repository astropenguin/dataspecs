__all__ = ["Tag"]


# standard library
from enum import Enum


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
