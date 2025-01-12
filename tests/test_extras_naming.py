# standard library
from dataclasses import dataclass
from enum import auto
from typing import Annotated


# dependencies
from dataspecs import Name, TagBase, from_dataclass, name


# test datasets
class Tag(TagBase):
    A = auto()


@dataclass
class Data:
    a: Annotated[int, Name("a!")]
    b: Annotated[int, Name("b!")]


# test functions
def test_name() -> None:
    specs = from_dataclass(Data(0, 1))
    named = name(specs)

    assert named[0].name == "a!"
    assert named[2].name == "b!"
