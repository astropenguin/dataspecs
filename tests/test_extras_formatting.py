# standard library
from dataclasses import dataclass
from enum import auto
from typing import Annotated, Optional


# dependencies
from dataspecs import TagBase, from_dataclass
from dataspecs.extras import Format, format


# test datasets
class Tag(TagBase):
    A = auto()


@dataclass
class Test:
    a: Annotated[str, Tag.A]
    b: Annotated[Optional[int], Format("/a", "data")] = None


# test functions
def test_replace() -> None:
    specs = from_dataclass(Test("{0}", 1))
    formatted = format(specs)

    assert formatted[0].data == "1"


def test_replace_skip() -> None:
    specs = from_dataclass(Test("{0}", None))
    formatted = format(specs)

    assert formatted[0].data == "{0}"
