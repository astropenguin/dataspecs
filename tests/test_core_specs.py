# standard library
from enum import auto
from typing import Any, Optional


# dependencies
from dataspecs.core.specs import ID, Spec, Specs
from dataspecs.core.typing import TagBase
from pytest import mark, raises


# type hints
TestData = list[tuple[Any, ...]]


# test datasets
class Tag(TagBase):
    DATA = auto()
    NAME = auto()
    UNITS = auto()


specs = [
    Spec(ID("/aaa"), (Tag.DATA,), None, None),
    Spec(ID("/aaa/name"), (Tag.NAME,), None, None),
    Spec(ID("/aaa/units"), (Tag.UNITS,), None, None),
    Spec(ID("/bbb"), (Tag.DATA,), None, None),
    Spec(ID("/bbb/name"), (Tag.NAME,), None, None),
    Spec(ID("/bbb/units"), (Tag.UNITS,), None, None),
    Spec(ID("/ccc"), (), None, None),
]

data_id_init: TestData = [
    ("/", True),
    ("/aaa", True),
    ("", ValueError),
    ("aaa", ValueError),
]

data_id_match: TestData = [
    ("/", "/", True),
    ("/", "/*", True),
    ("/", "/**", True),
    ("/", "*", False),
    ("/", "**", True),
    ("/", "aaa", False),
    #
    ("/aaa", "/*", True),
    ("/aaa", "/**", True),
    ("/aaa", "/aaa", True),
    ("/aaa", "*", False),
    ("/aaa", "**", True),
    ("/aaa", "aaa", False),
    #
    ("/aaa/bbb", "/*", False),
    ("/aaa/bbb", "/**", True),
    ("/aaa/bbb", "/aaa/*", True),
    ("/aaa/bbb", "/*/bbb", True),
    ("/aaa/bbb", "/aaa/bbb", True),
    ("/aaa/bbb", "*", False),
    ("/aaa/bbb", "**", True),
    ("/aaa/bbb", "aaa/*", False),
    ("/aaa/bbb", "*/bbb", False),
    ("/aaa/bbb", "aaa/bbb", False),
]

data_specs_first: TestData = [
    (specs, specs[0]),
    (specs[3:6], specs[3]),
    (specs[1:2], specs[1]),
    (specs[0:0], None),
]

data_specs_last: TestData = [
    (specs, specs[-1]),
    (specs[3:6], specs[5]),
    (specs[1:2], specs[1]),
    (specs[0:0], None),
]

data_specs_unique: TestData = [
    (specs, None),
    (specs[3:6], None),
    (specs[1:2], specs[1]),
    (specs[0:0], None),
]

data_specs_getitem: TestData = [
    (None, specs),
    #
    (Tag.DATA, [specs[0], specs[3]]),
    (Tag.NAME, [specs[1], specs[4]]),
    (Tag.UNITS, [specs[2], specs[5]]),
    #
    ("/*", [specs[0], specs[3], *specs[6:]]),
    ("/**", specs),
    ("/*/*", [*specs[1:3], *specs[4:6]]),
    ("/aaa", specs[0:1]),
    ("/aaa/*", specs[1:3]),
    ("/aaa**", specs[0:3]),
    ("/bbb", specs[3:4]),
    ("/bbb/*", specs[4:6]),
    ("/bbb**", specs[3:6]),
    ("/ccc", specs[6:7]),
    ("/ccc/*", []),
    ("/ccc**", specs[6:7]),
    ("/*/name", [specs[1], specs[4]]),
    ("/*/units", [specs[2], specs[5]]),
    #
    (slice(None, None), specs),
    (slice(0, 2), specs[0:2]),
    (0, specs[0]),
    (-1, specs[-1]),
]

data_specs_sub: TestData = [
    (specs, []),
    (specs[3:6], [*specs[0:3], *specs[6:]]),
    (specs[1:2], [specs[0], *specs[2:]]),
    (specs[0:0], specs),
]


# test functions
@mark.parametrize("tester, expected", data_id_init)
def test_id_init(tester: str, expected: Any) -> None:
    if expected is ValueError:
        with raises(expected):
            ID(tester)
    else:
        assert ID(tester)


@mark.parametrize("id, tester, expected", data_id_match)
def test_id_match(id: str, tester: str, expected: bool) -> None:
    assert ID(id).match(tester) == expected


@mark.parametrize("tester, expected", data_specs_first)
def test_specs_first(
    tester: list[Spec[Any]],
    expected: Optional[Spec[Any]],
) -> None:
    assert Specs(tester).first == expected


@mark.parametrize("tester, expected", data_specs_last)
def test_specs_last(
    tester: list[Spec[Any]],
    expected: Optional[Spec[Any]],
) -> None:
    assert Specs(tester).last == expected


@mark.parametrize("tester, expected", data_specs_unique)
def test_specs_unique(
    tester: list[Spec[Any]],
    expected: Optional[Spec[Any]],
) -> None:
    assert Specs(tester).unique == expected


@mark.parametrize("tester, expected", data_specs_getitem)
def test_specs_getitem(tester: Any, expected: Any) -> None:
    assert Specs(specs)[tester] == expected


@mark.parametrize("tester, expected", data_specs_sub)
def test_specs_sub(tester: Any, expected: Any) -> None:
    assert Specs(specs) - tester == expected
