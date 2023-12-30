__all__ = ["Category"]


# standard library
from enum import Enum


class Category(str, Enum):
    """Base string enum for categories."""

    @staticmethod
    def _generate_next_value_(
        name: str,
        start: int,
        count: int,
        last_values: list[str],
    ) -> str:
        return name.lower()
