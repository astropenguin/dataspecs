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


specs_simple: Specs[Spec[Any]] = Specs(
    [
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
            id=ID("/temp/name"),
            tags=(Tag.NAME,),
            type=str,
            data="Temperature",
        ),
        Spec(
            id=ID("/temp/units"),
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
            id=ID("/humid/name"),
            tags=(Tag.NAME,),
            type=str,
            data="Humidity",
        ),
        Spec(
            id=ID("/humid/units"),
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
            id=ID("/lon/name"),
            tags=(Tag.NAME,),
            type=str,
            data="Longitude",
        ),
        Spec(
            id=ID("/lon/units"),
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
            id=ID("/lat/name"),
            tags=(Tag.NAME,),
            type=str,
            data="Latitude",
        ),
        Spec(
            id=ID("/lat/units"),
            tags=(Tag.UNITS,),
            type=str,
            data="deg",
        ),
    ]
)


specs_full: Specs[Spec[Any]] = Specs(
    [
        Spec(
            id=ID("/temp"),
            tags=(),
            type=Union[list[float], float],
            data=[10, 20],
        ),
        Spec(
            id=ID("/temp/0"),
            tags=(Tag.DATA,),
            type=list[float],
            data=None,
        ),
        Spec(
            id=ID("/temp/0/0"),
            tags=(Tag.DTYPE,),
            type=float,
            data=None,
        ),
        Spec(
            id=ID("/temp/0/name"),
            tags=(Tag.NAME,),
            type=str,
            data="Temperature",
        ),
        Spec(
            id=ID("/temp/0/units"),
            tags=(Tag.UNITS,),
            type=str,
            data="K",
        ),
        Spec(
            id=ID("/temp/1"),
            tags=(),
            type=float,
            data=None,
        ),
        #
        Spec(
            id=ID("/humid"),
            tags=(),
            type=Union[list[float], float],
            data=[30, 40],
        ),
        Spec(
            id=ID("/humid/0"),
            tags=(Tag.DATA,),
            type=list[float],
            data=None,
        ),
        Spec(
            id=ID("/humid/0/0"),
            tags=(Tag.DTYPE,),
            type=float,
            data=None,
        ),
        Spec(
            id=ID("/humid/0/name"),
            tags=(Tag.NAME,),
            type=str,
            data="Humidity",
        ),
        Spec(
            id=ID("/humid/0/units"),
            tags=(Tag.UNITS,),
            type=str,
            data="%",
        ),
        Spec(
            id=ID("/humid/1"),
            tags=(),
            type=float,
            data=None,
        ),
        Spec(
            id=ID("/lon"),
            tags=(Tag.ATTR,),
            type=float,
            data=0.0,
        ),
        Spec(
            id=ID("/lon/name"),
            tags=(Tag.NAME,),
            type=str,
            data="Longitude",
        ),
        Spec(
            id=ID("/lon/units"),
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
            id=ID("/lat/name"),
            tags=(Tag.NAME,),
            type=str,
            data="Latitude",
        ),
        Spec(
            id=ID("/lat/units"),
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


def test_from_dataclass_simple() -> None:
    weather = Weather([10, 20], [30, 40])
    specs = from_dataclass(weather, first_only=True, tagged_only=True)
    assert specs == specs_simple


def test_from_dataclass_full() -> None:
    weather = Weather([10, 20], [30, 40])
    specs = from_dataclass(weather, first_only=False, tagged_only=False)
    assert specs == specs_full
