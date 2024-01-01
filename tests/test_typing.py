# standard library
from dataclasses import dataclass
from enum import auto
from typing import Annotated as Ann


# dependencies
from dataspecs.typing import Use as Use_, is_specclass


# test data
class Use(Use_):
    A = auto()
    B = auto()
    C = auto()


@dataclass
class SpecClass1:
    a: Ann[int, Use.A]


@dataclass
class SpecClass2:
    b: Ann[int, Use.B]
    c: Ann[int, Use.C]


@dataclass
class SpecClass3:
    a: Ann[int, Use.A, SpecClass2(1, 1)]


def test_use_comparison() -> None:
    assert Use.A == str("a")
    assert Use("a") is Use.A


def test_use_annotation() -> None:
    assert Use.annotates(Ann[int, Use.A])
    assert Use.annotates(Ann[int, Use.A])


def test_is_specclass() -> None:
    assert is_specclass(SpecClass1)
    assert is_specclass(SpecClass2)
    assert is_specclass(SpecClass3)
