__all__ = ["ID", "ROOT", "TagBase"]


# standard library
from dataclasses import Field, is_dataclass
from enum import Enum
from os import PathLike, fspath
from pathlib import PurePosixPath
from re import Match, compile, fullmatch
from typing import Annotated, Any, ClassVar, Protocol, Union, cast


# dependencies
from typing_extensions import TypeGuard, get_args, get_origin


# type hints
StrPath = Union[str, PathLike[str]]


# constants
GLOB_PATTERN = compile(r"\*\*()|\*([^\*]|$)")
GLOB_REPLS = r".*", r"[^/]*"


class ID(PurePosixPath):
    """Identifier (ID) for data specs.

    It is based on ``PurePosixPath``, however,
    the difference is an ID must start with the root (``/``).

    Args:
        *segments: Path segments to create an ID.

    Raises:
        ValueError: Raised if it does not start with the root.

    """

    def __init__(self, *segments: StrPath) -> None:
        super().__init__(*segments)

        if not self.root:
            raise ValueError("ID must start with the root.")

    def matches(self, path_pattern: StrPath, /) -> bool:
        """Check if the ID matches a path pattern.

        Unlike ``ID.match``, it also accepts double-wildcards
        (``**``) for recursively matching the path segments.

        Args:
            path_pattern: Path pattern for matching.

        Returns:
            ``True`` if the path pattern matches the ID.
            ``False`` otherwise.

        """

        def repl(match: Match[str]) -> str:
            index = cast(int, match.lastindex)
            return GLOB_REPLS[index - 1] + match.group(index)

        regex = GLOB_PATTERN.sub(repl, fspath(path_pattern))
        return bool(fullmatch(regex, fspath(self)))


ROOT = ID("/")
"""Root ID."""


# type hints
class DataClass(Protocol):
    """Type hint for any dataclass object."""

    __dataclass_fields__: ClassVar[dict[str, Field[Any]]]


class TagBase(Enum):
    """Tag base for data specifications.

    Since ``TagBase`` itself has no members,
    users should create their own tags by inheriting it::

            from enum import auto
            from dataspecs import TagBase

            class Tag(TagBase):
                ATTR = auto()
                DATA = auto()
                NAME = auto()

    """

    pass


def get_annotated(hint: Any, /) -> Any:
    """Return annotated type of a type hint if it exists."""
    return get_args(hint)[0] if is_annotated(hint) else hint


def get_annotations(hint: Any, /) -> tuple[Any, ...]:
    """Return annotations of a type hint if they exist."""
    return get_args(hint)[1:] if is_annotated(hint) else ()


def get_dataclasses(hint: Any, /) -> tuple[DataClass, ...]:
    """Return dataclass objects that annotate a type hint."""
    return tuple(filter(is_dataclass, get_annotations(hint)))


def get_subscriptions(hint: Any, /) -> tuple[Any, ...]:
    """Return subscriptions of a type hint if they exist."""
    return get_args(get_annotated(hint))


def get_tags(hint: Any, /) -> tuple[TagBase, ...]:
    """Return tags that annotate a type hint."""
    return tuple(filter(is_tag, get_annotations(hint)))


def is_annotated(hint: Any, /) -> bool:
    """Check if a type hint is annotated."""
    return get_origin(hint) is Annotated


def is_strpath(obj: Any, /) -> TypeGuard[StrPath]:
    """Check if an object is a string or a string path."""
    return isinstance(obj, (str, PathLike))


def is_tag(obj: Any, /) -> TypeGuard[TagBase]:
    """Check if an object is a specification tag."""
    return isinstance(obj, TagBase)
