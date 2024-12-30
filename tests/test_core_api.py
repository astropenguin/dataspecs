# standard library
from dataclasses import dataclass
from enum import auto
from typing import Annotated as Ann, Any, TypeVar, Union


# dependencies
from dataspecs.core.api import from_dataclass
from dataspecs.core.specs import ID, Spec, Specs
from dataspecs.core.typing import TagBase


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
    temp: Union[Ann[Data[float], Quantity("Temperature", "K")], float] = 0.0
    humid: Union[Ann[Data[float], Quantity("Humidity", "%")], float] = 0.0
    lon: Ann[Attr[float], Quantity("Longitude", "deg")] = 0.0
    lat: Ann[Attr[float], Quantity("Latitude", "deg")] = 0.0
    memo: str = "Observed in Tokyo"


specs: Specs[Spec[Any]] = Specs(
    [
        Spec(
            id=ID("/"),
            type=Weather,
            data=Weather([10, 20], [30, 40]),
        ),
        Spec(
            id=ID("/temp"),
            type=list[float],
            data=[10, 20],
            tags=(Tag.DATA,),
        ),
        Spec(
            id=ID("/temp/0"),
            type=float,
            data=None,
            tags=(Tag.DTYPE,),
        ),
        Spec(
            id=ID("/temp/quantity"),
            type=Quantity,
            data=Quantity("Temperature", "K"),
        ),
        Spec(
            id=ID("/temp/quantity/name"),
            type=str,
            data="Temperature",
            tags=(Tag.NAME,),
        ),
        Spec(
            id=ID("/temp/quantity/units"),
            type=str,
            data="K",
            tags=(Tag.UNITS,),
        ),
        Spec(
            id=ID("/humid"),
            type=list[float],
            data=[30, 40],
            tags=(Tag.DATA,),
        ),
        Spec(
            id=ID("/humid/0"),
            type=float,
            data=None,
            tags=(Tag.DTYPE,),
        ),
        Spec(
            id=ID("/humid/quantity"),
            type=Quantity,
            data=Quantity("Humidity", "%"),
        ),
        Spec(
            id=ID("/humid/quantity/name"),
            type=str,
            data="Humidity",
            tags=(Tag.NAME,),
        ),
        Spec(
            id=ID("/humid/quantity/units"),
            type=str,
            data="%",
            tags=(Tag.UNITS,),
        ),
        Spec(
            id=ID("/lon"),
            type=float,
            data=0.0,
            tags=(Tag.ATTR,),
        ),
        Spec(
            id=ID("/lon/quantity"),
            type=Quantity,
            data=Quantity("Longitude", "deg"),
        ),
        Spec(
            id=ID("/lon/quantity/name"),
            type=str,
            data="Longitude",
            tags=(Tag.NAME,),
        ),
        Spec(
            id=ID("/lon/quantity/units"),
            type=str,
            data="deg",
            tags=(Tag.UNITS,),
        ),
        Spec(
            id=ID("/lat"),
            type=float,
            data=0.0,
            tags=(Tag.ATTR,),
        ),
        Spec(
            id=ID("/lat/quantity"),
            type=Quantity,
            data=Quantity("Latitude", "deg"),
        ),
        Spec(
            id=ID("/lat/quantity/name"),
            type=str,
            data="Latitude",
            tags=(Tag.NAME,),
        ),
        Spec(
            id=ID("/lat/quantity/units"),
            type=str,
            data="deg",
            tags=(Tag.UNITS,),
        ),
        Spec(
            id=ID("/memo"),
            type=str,
            data="Observed in Tokyo",
        ),
    ]
)


def test_from_dataclass() -> None:
    assert from_dataclass(Weather([10, 20], [30, 40])) == specs
