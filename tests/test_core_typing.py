# standard library
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from typing import Annotated as Ann, Any, Literal, Optional, Union


# dependencies
from dataspecs.core.typing import (
    TagBase,
    get_annotated,
    get_annotations,
    get_dataclasses,
    get_first,
    get_subtypes,
    get_tags,
    is_annotated,
    is_literal,
    is_strpath,
    is_tag,
    is_union,
)
from pytest import mark


# type hints
TestData = list[tuple[Any, ...]]


# test datasets
class NonTag(Enum):
    A = auto()
    B = auto()


class Tag(TagBase):
    A = auto()
    B = auto()


@dataclass
class DC:
    a: int


data_get_annotated: TestData = [
    (Ann[int, "ann"], int),
    (int, int),
]

data_get_annotations: TestData = [
    (Ann[int, DC(1), DC(2)], (DC(1), DC(2))),
    (Ann[int, DC(1), Tag.A], (DC(1), Tag.A)),
    (Ann[int, DC(1)], (DC(1),)),
    (int, ()),
]

data_get_dataclasses: TestData = [
    (Ann[int, DC(1), DC(2)], (DC(1), DC(2))),
    (Ann[int, DC(1), Tag.A], (DC(1),)),
    (Ann[int, DC(1)], (DC(1),)),
    (int, ()),
]

data_get_first: TestData = [
    (Union[int, None], int),
    (Optional[int], int),
    (int, int),
]

data_get_subtypes: TestData = [
    (Union[str, int], (str, int)),
    (dict[str, int], (str, int)),
    (list[int], (int,)),
    (Literal[1], ()),
    (int, ()),
]

data_get_tags: TestData = [
    (Ann[int, Tag.A, Tag.B], (Tag.A, Tag.B)),
    (Ann[int, Tag.A, NonTag.B], (Tag.A,)),
    (Ann[int, Tag.A], (Tag.A,)),
    (Ann[int, NonTag.A], ()),
]

data_is_annotated: TestData = [
    (Ann[int, "ann"], True),
    (int, False),
]

data_is_literal: TestData = [
    (Literal[1], True),
    (1, False),
]

data_is_strpath: TestData = [
    ("path", True),
    (Path("path"), True),
    (b"path", False),
    (1, False),
]

data_is_tag: TestData = [
    (Tag.A, True),
    (NonTag.A, False),
    (1, False),
]

data_is_union: TestData = [
    (Ann[Union[int, None], "ann"], False),
    (Union[int, None], True),
    (int, False),
]


# test functions
@mark.parametrize("tester, expected", data_get_annotated)
def test_get_annotated(tester: Any, expected: Any) -> None:
    assert get_annotated(tester) == expected


@mark.parametrize("tester, expected", data_get_annotations)
def test_get_annotations(tester: Any, expected: Any) -> None:
    assert get_annotations(tester) == expected


@mark.parametrize("tester, expected", data_get_dataclasses)
def test_get_dataclasses(tester: Any, expected: Any) -> None:
    assert get_dataclasses(tester) == expected


@mark.parametrize("tester, expected", data_get_first)
def test_get_first(tester: Any, expected: Any) -> None:
    assert get_first(tester) == expected


@mark.parametrize("tester, expected", data_get_subtypes)
def test_get_subtypes(tester: Any, expected: Any) -> None:
    assert get_subtypes(tester) == expected


@mark.parametrize("tester, expected", data_get_tags)
def test_get_tags(tester: Any, expected: Any) -> None:
    assert get_tags(tester) == expected


@mark.parametrize("tester, expected", data_is_annotated)
def test_is_annotated(tester: Any, expected: bool) -> None:
    assert is_annotated(tester) == expected


@mark.parametrize("tester, expected", data_is_literal)
def test_is_literal(tester: Any, expected: bool) -> None:
    assert is_literal(tester) == expected


@mark.parametrize("tester, expected", data_is_strpath)
def test_is_strpath(tester: Any, expected: bool) -> None:
    assert is_strpath(tester) == expected


@mark.parametrize("tester, expected", data_is_tag)
def test_is_tag(tester: Any, expected: bool) -> None:
    assert is_tag(tester) == expected


@mark.parametrize("tester, expected", data_is_union)
def test_is_union(tester: Any, expected: Any) -> None:
    assert is_union(tester) == expected
