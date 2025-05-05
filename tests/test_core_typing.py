# standard library
from sys import version_info as ver
from typing import Annotated as Ann, Literal as L, Union


# dependencies
from dataspecs.core.typing import (
    gen_annotations,
    gen_subtypes,
    get_annotated,
    is_annotated,
    is_literal,
    is_union,
)


# test functions
def test_gen_annotations() -> None:
    assert list(gen_annotations(int)) == []
    assert list(gen_annotations(Ann[int, 0])) == [0]
    assert list(gen_annotations(Union[Ann[int, 0], Ann[int, 1]])) == [0, 1]
    assert list(gen_annotations(Ann[Union[Ann[int, 0], Ann[int, 1]], 2])) == [0, 1, 2]


def test_gen_subtypes() -> None:
    assert list(gen_subtypes(int)) == []
    assert list(gen_subtypes(dict[str, int])) == [str, int]
    assert list(gen_subtypes(dict[str, L[0, 1]])) == [str, L[0, 1]]
    assert list(gen_subtypes(Union[dict[str, int], None])) == [str, int]


def test_get_annotated() -> None:
    assert get_annotated(int) == int
    assert get_annotated(Ann[int, 0]) == int
    assert get_annotated(Union[Ann[int, 0], Ann[int, 1]]) == int
    assert get_annotated(Ann[Union[Ann[int, 0], Ann[int, 1]], 2]) == int


def test_is_annotated() -> None:
    assert not is_annotated(int)
    assert is_annotated(Ann[int, 0])


def test_is_literal() -> None:
    assert not is_literal(int)
    assert is_literal(L[0])


def test_is_union() -> None:
    assert not is_union(int)
    assert is_union(Union[int, float])

    if ver.major >= 3 and ver.minor >= 10:
        assert is_union(int | float)
