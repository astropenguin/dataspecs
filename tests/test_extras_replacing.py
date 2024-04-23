# standard library
from dataclasses import dataclass
from enum import auto
from typing import Annotated, Optional


# dependencies
from dataspecs import TagBase, from_dataclass
from dataspecs.extras import Replace, replace


# test datasets
class Tag(TagBase):
    A = auto()


@dataclass
class Data:
    a: Annotated[float, Tag.A]
    a_type: Annotated[Optional[type], Replace("/a", "type")] = None
    a_data: Annotated[Optional[float], Replace("/a", "data")] = None


# test functions
def test_replace() -> None:
    specs = from_dataclass(Data(0, int, 1))
    replaced = replace(specs)

    assert replaced[0].type is int
    assert replaced[0].data == 1


def test_replace_skip() -> None:
    specs = from_dataclass(Data(0, None, None))
    replaced = replace(specs)

    assert replaced[0].type is float
    assert replaced[0].data == 0
