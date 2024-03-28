# standard library
from dataclasses import dataclass
from enum import auto
from typing import Annotated as Ann, Any, TypeVar


# dependencies
from dataspecs.api import from_dataclass, from_typehint
from dataspecs.specs import ID, Spec, Specs
from dataspecs.typing import TagBase


# type hints
class Tag(TagBase):
    ATTR = auto()
    DATA = auto()
    DTYPE = auto()
    NAME = auto()
    UNITS = auto()


T = TypeVar("T")
Attr = Ann[T, Tag.ATTR]
Data = Ann[list[Ann[T, Tag.DTYPE]], Tag.DATA]


# test datasets
@dataclass(frozen=True)
class Quantity:
    name: Ann[str, Tag.NAME]
    units: Ann[str, Tag.UNITS]


@dataclass(frozen=True)
class Weather:
    temp: Ann[Data[float], Quantity("Temperature", "K")]
    humid: Ann[Data[float], Quantity("Humidity", "%")]
    lon: Ann[Attr[float], Quantity("Longitude", "deg")] = 0.0
    lat: Ann[Attr[float], Quantity("Latitude", "deg")] = 0.0
    memo: str = "Observed in Tokyo"


specs = Specs(
    [
        Spec(
            id=ID("/temp"),
            tags=(Tag.DATA,),
            data=[10, 20],
            type=Ann[Data[float], Quantity("Temperature", "K")],
            origin=Weather([10, 20], [30, 40]),
        ),
        Spec(
            id=ID("/temp/0"),
            tags=(Tag.DTYPE,),
            data=float,
            type=Any,
            origin=Ann[Data[float], Quantity("Temperature", "K")],
        ),
        Spec(
            id=ID("/temp/name"),
            tags=(Tag.NAME,),
            data="Temperature",
            type=Ann[str, Tag.NAME],
            origin=Quantity(name="Temperature", units="K"),
        ),
        Spec(
            id=ID("/temp/units"),
            tags=(Tag.UNITS,),
            data="K",
            type=Ann[str, Tag.UNITS],
            origin=Quantity(name="Temperature", units="K"),
        ),
        Spec(
            id=ID("/humid"),
            tags=(Tag.DATA,),
            data=[30, 40],
            type=Ann[Data[float], Quantity("Humidity", "%")],
            origin=Weather([10, 20], [30, 40]),
        ),
        Spec(
            id=ID("/humid/0"),
            tags=(Tag.DTYPE,),
            data=float,
            type=Any,
            origin=Ann[Data[float], Quantity("Humidity", "%")],
        ),
        Spec(
            id=ID("/humid/name"),
            tags=(Tag.NAME,),
            data="Humidity",
            type=Ann[str, Tag.NAME],
            origin=Quantity(name="Humidity", units="%"),
        ),
        Spec(
            id=ID("/humid/units"),
            tags=(Tag.UNITS,),
            data="%",
            type=Ann[str, Tag.UNITS],
            origin=Quantity(name="Humidity", units="%"),
        ),
        Spec(
            id=ID("/lon"),
            tags=(Tag.ATTR,),
            data=0.0,
            type=Ann[Attr[float], Quantity("Longitude", "deg")],
            origin=Weather([10, 20], [30, 40]),
        ),
        Spec(
            id=ID("/lon/name"),
            tags=(Tag.NAME,),
            data="Longitude",
            type=Ann[str, Tag.NAME],
            origin=Quantity("Longitude", "deg"),
        ),
        Spec(
            id=ID("/lon/units"),
            tags=(Tag.UNITS,),
            data="deg",
            type=Ann[str, Tag.UNITS],
            origin=Quantity("Longitude", "deg"),
        ),
        Spec(
            id=ID("/lat"),
            tags=(Tag.ATTR,),
            data=0.0,
            type=Ann[Attr[float], Quantity("Latitude", "deg")],
            origin=Weather([10, 20], [30, 40]),
        ),
        Spec(
            id=ID("/lat/name"),
            tags=(Tag.NAME,),
            data="Latitude",
            type=Ann[str, Tag.NAME],
            origin=Quantity("Latitude", "deg"),
        ),
        Spec(
            id=ID("/lat/units"),
            tags=(Tag.UNITS,),
            data="deg",
            type=Ann[str, Tag.UNITS],
            origin=Quantity("Latitude", "deg"),
        ),
        Spec(
            id=ID("/memo"),
            tags=(),
            data="Observed in Tokyo",
            type=str,
            origin=Weather([10, 20], [30, 40]),
        ),
    ]
)


def test_from_dataclass() -> None:
    assert from_dataclass(Weather([10, 20], [30, 40])) == specs


def test_from_typehint() -> None:
    hint_temp = Ann[Data[float], Quantity("Temperature", "K")]
    hint_humid = Ann[Data[float], Quantity("Humidity", "%")]
    hint_lon = Ann[Attr[float], Quantity("Longitude", "deg")]
    hint_lat = Ann[Attr[float], Quantity("Latitude", "deg")]

    assert from_typehint(hint_temp, parent_id="/temp") == specs[1:4]
    assert from_typehint(hint_humid, parent_id="/humid") == specs[5:8]
    assert from_typehint(hint_lon, parent_id="/lon") == specs[9:11]
    assert from_typehint(hint_lat, parent_id="/lat") == specs[12:14]
