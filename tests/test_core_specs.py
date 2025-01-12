# standard library
from enum import auto
from typing import Any, Optional


# dependencies
from dataspecs.core.specs import ID, SpecAttr, Spec, Specs
from dataspecs.core.typing import TagBase
from pytest import mark, raises


# type hints
TestData = list[tuple[Any, ...]]


# test datasets
class Tag(TagBase):
    DATA = auto()
    NAME = auto()
    UNITS = auto()


specs = Specs(
    [
        Spec(ID("/a"), "a", (Tag.DATA,), int, None),
        Spec(ID("/a/name"), "name", (Tag.NAME,), str, None),
        Spec(ID("/a/units"), "units", (Tag.UNITS,), str, None),
        Spec(ID("/b"), "b", (Tag.DATA,), int, None),
        Spec(ID("/b/name"), "name", (Tag.NAME,), str, None),
        Spec(ID("/b/units"), "units", (Tag.UNITS,), str, None),
        Spec(ID("/c"), "c", (), int, None),
    ]
)

data_id_init: TestData = [
    ("/", True),
    ("/a", True),
    ("", ValueError),
    ("a", ValueError),
]

data_id_match: TestData = [
    (ID("/"), "/", True),
    (ID("/"), "/.*", True),
    (ID("/"), ".*", True),
    (ID("/"), "/a", False),
    #
    (ID("/a"), "/a", True),
    (ID("/a"), "/.*", True),
    (ID("/a"), ".*", True),
    (ID("/a"), "/b", False),
    #
    (ID("/a/b"), "/a/b", True),
    (ID("/a/b"), "/a/.*", True),
    (ID("/a/b"), "/.*/b", True),
    (ID("/a/b"), "/.*/.*", True),
    (ID("/a/b"), "/.*", True),
    (ID("/a/b"), ".*", True),
    (ID("/a/b"), "/a/c", False),
    (ID("/a/b"), "/c/b", False),
    (ID("/a/b"), "/c/d", False),
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

data_specs_groupby: TestData = [
    (
        "id",
        [
            specs[0:1],
            specs[1:2],
            specs[2:3],
            specs[3:4],
            specs[4:5],
            specs[5:6],
            specs[6:7],
        ],
    ),
    (
        "tags",
        [
            Specs([specs[0], specs[3]]),
            Specs([specs[1], specs[4]]),
            Specs([specs[2], specs[5]]),
            Specs([specs[6]]),
        ],
    ),
    (
        "type",
        [
            Specs([specs[0], specs[3], specs[6]]),
            Specs([*specs[1:3], *specs[4:6]]),
        ],
    ),
    (
        "data",
        [specs],
    ),
]

data_specs_replace: TestData = [
    (specs[0], [*specs[0:6], specs[0]]),
    (specs[1], [*specs[0:6], specs[1]]),
    (specs[-1], specs),
]

data_specs_getitem: TestData = [
    (None, specs),
    #
    (Tag.DATA, [specs[0], specs[3]]),
    (Tag.NAME, [specs[1], specs[4]]),
    (Tag.UNITS, [specs[2], specs[5]]),
    #
    (Tag, specs[0:6]),
    #
    (int, [specs[0], specs[3], specs[6]]),
    (str, [specs[1], specs[2], specs[4], specs[5]]),
    #
    ("/.*", specs),
    ("/[^/]*", [specs[0], specs[3], specs[6]]),
    ("/.*/.*", [*specs[1:3], *specs[4:6]]),
    ("/a", specs[0:1]),
    ("/a/.*", specs[1:3]),
    ("/a.*", specs[0:3]),
    ("/b", specs[3:4]),
    ("/b/.*", specs[4:6]),
    ("/b.*", specs[3:6]),
    ("/c", specs[6:7]),
    ("/c/.*", []),
    ("/c.*", specs[6:7]),
    ("/.*/name", [specs[1], specs[4]]),
    ("/.*/units", [specs[2], specs[5]]),
    #
    (slice(None, None), specs),
    (slice(0, 2), specs[0:2]),
    (0, specs[0]),
    (-1, specs[-1]),
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
def test_id_match(id: ID, tester: str, expected: bool) -> None:
    assert id.match(tester) == expected


@mark.parametrize("tester, expected", data_specs_first)
def test_specs_first(tester: Specs[Spec[Any]], expected: Optional[Spec[Any]]) -> None:
    assert tester.first == expected


@mark.parametrize("tester, expected", data_specs_last)
def test_specs_last(tester: Specs[Spec[Any]], expected: Optional[Spec[Any]]) -> None:
    assert tester.last == expected


@mark.parametrize("tester, expected", data_specs_unique)
def test_specs_unique(tester: Specs[Spec[Any]], expected: Optional[Spec[Any]]) -> None:
    assert tester.unique == expected


@mark.parametrize("tester, expected", data_specs_groupby)
def test_specs_groupby(tester: SpecAttr, expected: list[Specs[Spec[Any]]]) -> None:
    assert specs.groupby(tester) == expected


@mark.parametrize("tester, expected", data_specs_replace)
def test_specs_replace(tester: Spec[Any], expected: list[Specs[Spec[Any]]]) -> None:
    assert specs.replace(specs[-1], tester) == expected


@mark.parametrize("tester, expected", data_specs_getitem)
def test_specs_getitem(tester: Any, expected: Any) -> None:
    assert specs[tester] == expected
