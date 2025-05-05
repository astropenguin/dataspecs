# standard library
from collections.abc import Hashable
from dataclasses import dataclass
from typing import Annotated as Ann, ClassVar, Optional, TypeVar


# dependencies
from dataspecs import ID, Name, Spec, Specs, Tag, Unit, from_dataclass


# type hints
TAny = TypeVar("TAny")
Dtype = Ann[TAny, ID("dtype"), Tag("meta")]


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
            name="Description",
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
            name="Description",
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
@dataclass
class Data:
    """Type annotation for measured data."""

    tag: ClassVar[Tag] = Tag("data")

    name: Name
    """Name of the measured data."""

    unit: Unit
    """Optional unit of the measured data."""

    desc: Ann[Optional[str], Name("Description"), Tag("meta")]
    """Optional description of the measured data."""

    def __init__(
        self,
        name: Hashable,
        unit: Optional[str] = None,
        desc: Optional[str] = None,
        /,
    ) -> None:
        self.name = Name(name)
        self.unit = Unit(unit)
        self.desc = desc


@dataclass
class Weather:
    temp: Ann[
        list[Dtype[float]],
        Data(
            "Temperature",
            "deg C",
            "Air temperature measured at 1.5 m above the ground.",
        ),
    ]
    wind: Ann[
        list[Dtype[float]],
        Data(
            "Wind speed",
            "m s^-1",
            "Wind speed measured at 1.5 m above the ground.",
        ),
    ]
    site: Ann[str, Tag("meta"), Name("Observation site")] = "Tokyo"


def test_from_dataclass() -> None:
    assert from_dataclass(Weather([20.0, 25.0], [3.0, 6.0])) == SPECS
