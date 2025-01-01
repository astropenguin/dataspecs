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
            tags=(),
            type=Weather,
            data=Weather([10, 20], [30, 40]),
        ),
        Spec(
            id=ID("/temp"),
            tags=(Tag.DATA,),
            type=list[float],
            data=[10, 20],
        ),
        Spec(
            id=ID("/temp/0"),
            tags=(Tag.DTYPE,),
            type=float,
            data=None,
        ),
        Spec(
            id=ID("/temp/quantity"),
            tags=(),
            type=Quantity,
            data=Quantity("Temperature", "K"),
        ),
        Spec(
            id=ID("/temp/quantity/name"),
            tags=(Tag.NAME,),
            type=str,
            data="Temperature",
        ),
        Spec(
            id=ID("/temp/quantity/units"),
            tags=(Tag.UNITS,),
            type=str,
            data="K",
        ),
        Spec(
            id=ID("/humid"),
            tags=(Tag.DATA,),
            type=list[float],
            data=[30, 40],
        ),
        Spec(
            id=ID("/humid/0"),
            tags=(Tag.DTYPE,),
            type=float,
            data=None,
        ),
        Spec(
            id=ID("/humid/quantity"),
            tags=(),
            type=Quantity,
            data=Quantity("Humidity", "%"),
        ),
        Spec(
            id=ID("/humid/quantity/name"),
            tags=(Tag.NAME,),
            type=str,
            data="Humidity",
        ),
        Spec(
            id=ID("/humid/quantity/units"),
            tags=(Tag.UNITS,),
            type=str,
            data="%",
        ),
        Spec(
            id=ID("/lon"),
            tags=(Tag.ATTR,),
            type=float,
            data=0.0,
        ),
        Spec(
            id=ID("/lon/quantity"),
            tags=(),
            type=Quantity,
            data=Quantity("Longitude", "deg"),
        ),
        Spec(
            id=ID("/lon/quantity/name"),
            tags=(Tag.NAME,),
            type=str,
            data="Longitude",
        ),
        Spec(
            id=ID("/lon/quantity/units"),
            tags=(Tag.UNITS,),
            type=str,
            data="deg",
        ),
        Spec(
            id=ID("/lat"),
            tags=(Tag.ATTR,),
            type=float,
            data=0.0,
        ),
        Spec(
            id=ID("/lat/quantity"),
            tags=(),
            type=Quantity,
            data=Quantity("Latitude", "deg"),
        ),
        Spec(
            id=ID("/lat/quantity/name"),
            tags=(Tag.NAME,),
            type=str,
            data="Latitude",
        ),
        Spec(
            id=ID("/lat/quantity/units"),
            tags=(Tag.UNITS,),
            type=str,
            data="deg",
        ),
        Spec(
            id=ID("/memo"),
            tags=(),
            type=str,
            data="Observed in Tokyo",
        ),
    ]
)


def test_from_dataclass() -> None:
    assert from_dataclass(Weather([10, 20], [30, 40])) == specs
