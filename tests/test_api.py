# standard library
from dataclasses import dataclass
from pathlib import PurePosixPath as Path
from typing import Annotated as Ann, TypeVar


# dependencies
from dataspecs import ID, Data, Name, Spec, Specs, Tag, from_dataclass


# type hints
T = TypeVar("T")
Dtype = Ann[T, ID("dtype"), Tag("dtype")]


# constants
SPECS = Specs(
    [
        Spec(
            data=[20.0, 25.0],
            id=Path("/temp"),
            name="Temperature",
            tags=frozenset({"data"}),
            type=list[float],
        ),
        Spec(
            data=None,
            id=Path("/temp/dtype"),
            name="dtype",
            tags=frozenset({"dtype"}),
            type=float,
        ),
        Spec(
            data="deg C",
            id=Path("/temp/units"),
            name="units",
            tags=frozenset({"attr"}),
            type=str,
        ),
        Spec(
            data="Air temperature measured at 1.5 m above the ground.",
            id=Path("/temp/long_name"),
            name="long_name",
            tags=frozenset({"attr"}),
            type=str,
        ),
        Spec(
            data=[3.0, 6.0],
            id=Path("/wind"),
            name="Wind speed",
            tags=frozenset({"data"}),
            type=list[float],
        ),
        Spec(
            data=None,
            id=Path("/wind/dtype"),
            name="dtype",
            tags=frozenset({"dtype"}),
            type=float,
        ),
        Spec(
            data="m/s",
            id=Path("/wind/units"),
            name="units",
            tags=frozenset({"attr"}),
            type=str,
        ),
        Spec(
            data="Wind speed measured at 1.5 m above the ground.",
            id=Path("/wind/long_name"),
            name="long_name",
            tags=frozenset({"attr"}),
            type=str,
        ),
        Spec(
            data="Tokyo",
            id=Path("/site"),
            name="Observation site",
            tags=frozenset({"attr"}),
            type=str,
        ),
        Spec(
            data=Data("K"),
            id=Path("/temp/units"),
            name="units",
            tags=frozenset(),
            type=Data,
        ),
        Spec(
            data=Data("km/h"),
            id=Path("/wind/units"),
            name="units",
            tags=frozenset(),
            type=Data,
        ),
    ]
)


@dataclass
class Meta:
    units: Ann[str, Tag("attr")]
    long_name: Ann[str, Tag("attr")]


@dataclass
class Weather:
    temp: Ann[
        list[Dtype[float]],
        Name("Temperature"),
        Tag("data"),
        Meta("deg C", "Air temperature measured at 1.5 m above the ground."),
    ]
    wind: Ann[
        list[Dtype[float]],
        Name("Wind speed"),
        Tag("data"),
        Meta("m/s", "Wind speed measured at 1.5 m above the ground."),
    ]
    site: Ann[str, Name("Observation site"), Tag("attr")]
    temp_units: Ann[Data, ID("/temp/units")] = Data("deg C")
    wind_units: Ann[Data, ID("/wind/units")] = Data("m/s")


def test_from_dataclass() -> None:
    obj = Weather([20.0, 25.0], [3.0, 6.0], "Tokyo", Data("K"), Data("km/h"))
    assert from_dataclass(obj, merge=False) == SPECS


def test_from_dataclass_merge() -> None:
    obj = Weather([20.0, 25.0], [3.0, 6.0], "Tokyo", Data("K"), Data("km/h"))
    assert from_dataclass(obj, merge=True)[2] == (Data("K") >> SPECS[2])
    assert from_dataclass(obj, merge=True)[6] == (Data("km/h") >> SPECS[6])
