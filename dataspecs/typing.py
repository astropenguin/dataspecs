__all__ = ["ID", "ROOT", "DataClass", "TagBase"]


# standard library
from dataclasses import Field, is_dataclass
from enum import Enum
from os import PathLike, fspath
from pathlib import PurePosixPath
from re import Match, fullmatch, sub
from typing import Annotated, Any, ClassVar, Protocol, Union, cast


# dependencies
from typing_extensions import TypeGuard, get_args, get_origin


# type hints
StrPath = Union[str, PathLike[str]]


# constants
GLOB_PATTERNS = r"\*\*()|\*([^\*]|$)"
GLOB_REPLS = r".*", r"[^/]*"


class ID(PurePosixPath):
    """Identifier (ID) for data specifications.

    It is based on ``PurePosixPath`` but an ID requires that
    (1) each path segment of it must be either an identifier
    of Python or a digit and (2) it must start with the root.

    Args:
        *segments: Path segments to create an ID.

    Raises:
        ValueError: Raised if (1) ID does not start with
            the root or (2) Each path segment is not neither
            an identifier of Python nor a digit.

    """

    def __init__(self, *segments: StrPath) -> None:
        super().__init__(*segments)

        if not self.root:
            raise ValueError("ID must start with the root.")

        for part in self.parts[1:]:
            if not (part.isidentifier() or part.isdigit()):
                raise ValueError(
                    "Each path segment must be either"
                    "an identifier of Python or a digit."
                )

    def matches(self, pattern: StrPath) -> bool:
        """Check if the ID matches a pattern.

        Unlike ``ID.match``, it also accepts double-wildcards
        (``**``) for recursively matching the path segments.

        Args:
            pattern: Pattern string or path-like object.

        Returns:
            ``True`` if the pattern matches the ID.
            ``False`` otherwise.

        """

        def repl(match: Match[str]) -> str:
            index = cast(int, match.lastindex)
            return GLOB_REPLS[index - 1] + match.group(index)

        converted = sub(GLOB_PATTERNS, repl, fspath(pattern))
        return bool(fullmatch(converted, fspath(self)))


ROOT = ID("/")
"""Root ID."""


# type hints
class DataClass(Protocol):
    """Type hint for any dataclass object."""

    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]


class TagBase(Enum):
    """Tag base for data specifications."""

    pass


def get_annotated(hint: Any) -> Any:
    """Return annotated type of a type hint if it exists."""
    return get_args(hint)[0] if is_annotated(hint) else hint


def get_annotations(hint: Any) -> tuple[Any, ...]:
    """Return annotations of a type hint if they exist."""
    return get_args(hint)[1:] if is_annotated(hint) else ()


def get_dataclasses(hint: Any) -> tuple[DataClass, ...]:
    """Return dataclass objects that annotate a type hint."""
    return tuple(filter(is_dataclass, get_annotations(hint)))


def get_subscriptions(hint: Any) -> tuple[Any, ...]:
    """Return subscriptions of a type hint if they exist."""
    return get_args(get_annotated(hint))


def get_tags(hint: Any) -> tuple[TagBase, ...]:
    """Return tags that annotate a type hint."""
    return tuple(filter(is_tag, get_annotations(hint)))


def is_annotated(hint: Any) -> bool:
    """Check if a type hint is annotated."""
    return get_origin(hint) is Annotated


def is_tag(obj: Any) -> TypeGuard[TagBase]:
    """Check if an object is a specification tag."""
    return isinstance(obj, TagBase)
