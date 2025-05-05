# standard library
from typing import Optional


# dependencies
from dataspecs import Data, ID, Name, Spec, Specs, Tag, Type, Unit


# constants
SPECS = Specs(
    [
        Spec(
            data=[20.0, 25.0],
            id="/temp",
            name="Temperature",
            tags=frozenset({"data"}),
            type=list[float],
            unit="deg C",
        ),
        Spec(
            data=None,
            id="/temp/dtype",
            name="dtype",
            tags=frozenset({"meta"}),
            type=float,
            unit=None,
        ),
        Spec(
            data="Air temperature measured at 1.5 m above the ground.",
            id="/temp/desc",
            name="description",
            tags=frozenset({"meta"}),
            type=Optional[str],
            unit=None,
        ),
        Spec(
            data=[3.0, 6.0],
            id="/wind",
            name="Wind speed",
            tags=frozenset({"data"}),
            type=list[float],
            unit="m s^-1",
        ),
        Spec(
            data=None,
            id="/wind/dtype",
            name="dtype",
            tags=frozenset({"meta"}),
            type=float,
            unit=None,
        ),
        Spec(
            data="Wind speed measured at 1.5 m above the ground.",
            id="/wind/desc",
            name="description",
            tags=frozenset({"meta"}),
            type=Optional[str],
            unit=None,
        ),
        Spec(
            data="Tokyo",
            id="/site",
            name="Observation site",
            tags=frozenset({"meta"}),
            type=str,
            unit=None,
        ),
    ]
)


# test functions
def test_specs_first() -> None:
    assert SPECS.first == SPECS[0]


def test_specs_last() -> None:
    assert SPECS.last == SPECS[-1]


def test_specs_unique() -> None:
    assert SPECS.unique is None


def test_specs_groupby() -> None:
    assert SPECS.groupby("id") == [
        Specs([SPECS[0]]),
        Specs([SPECS[1]]),
        Specs([SPECS[2]]),
        Specs([SPECS[3]]),
        Specs([SPECS[4]]),
        Specs([SPECS[5]]),
        Specs([SPECS[6]]),
    ]
    assert SPECS.groupby("name") == [
        Specs([SPECS[0]]),
        Specs([SPECS[1], SPECS[4]]),
        Specs([SPECS[2], SPECS[5]]),
        Specs([SPECS[3]]),
        Specs([SPECS[6]]),
    ]
    assert SPECS.groupby("tags") == [
        Specs([SPECS[0], SPECS[3]]),
        Specs([*SPECS[1:3], *SPECS[4:7]]),
    ]
    assert SPECS.groupby("type") == [
        Specs([SPECS[0], SPECS[3]]),
        Specs([SPECS[1], SPECS[4]]),
        Specs([SPECS[2], SPECS[5]]),
        Specs([SPECS[6]]),
    ]
    assert SPECS.groupby("unit") == [
        Specs([SPECS[0]]),
        Specs([*SPECS[1:3], *SPECS[4:7]]),
        Specs([SPECS[3]]),
    ]


def test_specs_replace() -> None:
    assert SPECS.replace(SPECS[0], SPECS[1]) == Specs([SPECS[1], *SPECS[1:]])


def test_specs_getitem() -> None:
    assert SPECS[Data([20.0, 25.0])] == Specs([SPECS[0]])
    assert SPECS[ID("/temp") == Specs([SPECS[0]])]
    assert SPECS[Name("Temperature") == Specs([SPECS[0]])]
    assert SPECS[Tag("data") == Specs([SPECS[0], SPECS[3]])]
    assert SPECS[Type(list[float]) == Specs([SPECS[0], SPECS[3]])]
    assert SPECS[Unit("deg C")] == Specs([SPECS[0]])
