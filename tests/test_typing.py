# standard library
from dataclasses import dataclass
from enum import auto
from typing import Annotated as Ann


# dependencies
from dataspecs.typing import SpecType, is_specclass


# test data
class Type(SpecType):
    A = auto()
    B = auto()
    C = auto()


@dataclass
class SpecClass1:
    a: Ann[int, Type.A]


@dataclass
class SpecClass2:
    b: Ann[int, Type.B]
    c: Ann[int, Type.C]


@dataclass
class SpecClass3:
    a: Ann[int, Type.A, SpecClass2(1, 1)]


def test_spectype_conversion() -> None:
    assert Type.A == str("a")
    assert Type("a") is Type.A


def test_spectype_annotates() -> None:
    assert SpecType.annotates(Ann[int, Type.A])
    assert Type.annotates(Ann[int, Type.A])


def test_is_specclass() -> None:
    assert is_specclass(SpecClass1)
    assert is_specclass(SpecClass2)
    assert is_specclass(SpecClass3)
