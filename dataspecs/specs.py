__all__ = ["Spec"]


# standard library
from dataclasses import Field, field as field_
from typing import Any, Final, Literal, Optional


# dependencies
from typing_extensions import Self


# type hints
Category = Literal[
    "attr",
    "data",
    "dims",
    "dtype",
    "factory",
    "index",
    "name",
    "root",
]


class Spec(dict[str, Any]):
    """Data specification for dataclasses."""

    ROOT_ID: Final = "/"
    """ID for the root of the specification."""

    @property
    def category(self) -> Category:
        """Category of the specification."""
        return self.root.get("category", "root")

    @property
    def default(self) -> Optional[Any]:
        """Default value of the specification."""
        return self.root.get("default", None)

    @property
    def field(self) -> Field[Any]:
        """Field of the specification."""
        return self.root.get("field", field_())

    @property
    def origin(self) -> Field[Any]:
        """Origin of the specification."""
        return self.root.get("origin", None)

    @property
    def type(self) -> Optional[Any]:
        """Type (hint) of the specification."""
        return self.root.get("type", None)

    @property
    def root(self) -> Self:
        """Root of the specification."""
        cls = type(self)

        return cls(
            (id, spec)
            for id, spec in self.items()
            if id == cls.ROOT_ID or not isinstance(spec, cls)
        )

    @property
    def nodes(self) -> Self:
        """Nodes of the specification."""
        cls = type(self)

        return cls(
            (id, spec)
            for id, spec in self.items()
            if id != cls.ROOT_ID and isinstance(spec, cls)
        )
