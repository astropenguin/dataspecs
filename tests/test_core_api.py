# standard library
from dataclasses import dataclass
from enum import auto
from typing import Annotated as Ann, Any, TypeVar, Union


# dependencies
from dataspecs.core.api import from_dataclass
from dataspecs.core.specs import Path, Spec, Specs
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
            path=Path("/temp"),
            name="temp",
            tags=(Tag.DATA,),
            type=list[float],
            data=[10, 20],
            anns=(Tag.DATA, Quantity("Temperature", "K")),
            orig=Weather([10, 20], [30, 40]),
        ),
        Spec(
            path=Path("/temp/0"),
            name="0",
            tags=(Tag.DTYPE,),
            type=float,
            data=None,
            anns=(Tag.DTYPE,),
            orig=Union[Ann[Data[float], Quantity("Temperature", "K")], float],
        ),
        Spec(
            path=Path("/temp/name"),
            name="name",
            tags=(Tag.NAME,),
            type=str,
            data="Temperature",
            anns=(Tag.NAME,),
            orig=Quantity("Temperature", "K"),
        ),
        Spec(
            path=Path("/temp/units"),
            name="units",
            tags=(Tag.UNITS,),
            type=str,
            data="K",
            anns=(Tag.UNITS,),
            orig=Quantity("Temperature", "K"),
        ),
        Spec(
            path=Path("/humid"),
            name="humid",
            tags=(Tag.DATA,),
            type=list[float],
            data=[30, 40],
            anns=(Tag.DATA, Quantity("Humidity", "%")),
            orig=Weather([10, 20], [30, 40]),
        ),
        Spec(
            path=Path("/humid/0"),
            name="0",
            tags=(Tag.DTYPE,),
            type=float,
            data=None,
            anns=(Tag.DTYPE,),
            orig=Union[Ann[Data[float], Quantity("Humidity", "%")], float],
        ),
        Spec(
            path=Path("/humid/name"),
            name="name",
            tags=(Tag.NAME,),
            type=str,
            data="Humidity",
            anns=(Tag.NAME,),
            orig=Quantity("Humidity", "%"),
        ),
        Spec(
            path=Path("/humid/units"),
            name="units",
            tags=(Tag.UNITS,),
            type=str,
            data="%",
            anns=(Tag.UNITS,),
            orig=Quantity("Humidity", "%"),
        ),
        Spec(
            path=Path("/lon"),
            name="lon",
            tags=(Tag.ATTR,),
            type=float,
            data=0.0,
            anns=(Tag.ATTR, Quantity("Longitude", "deg")),
            orig=Weather([10, 20], [30, 40]),
        ),
        Spec(
            path=Path("/lon/name"),
            name="name",
            tags=(Tag.NAME,),
            type=str,
            data="Longitude",
            anns=(Tag.NAME,),
            orig=Quantity("Longitude", "deg"),
        ),
        Spec(
            path=Path("/lon/units"),
            name="units",
            tags=(Tag.UNITS,),
            type=str,
            data="deg",
            anns=(Tag.UNITS,),
            orig=Quantity("Longitude", "deg"),
        ),
        Spec(
            path=Path("/lat"),
            name="lat",
            tags=(Tag.ATTR,),
            type=float,
            data=0.0,
            anns=(Tag.ATTR, Quantity("Latitude", "deg")),
            orig=Weather([10, 20], [30, 40]),
        ),
        Spec(
            path=Path("/lat/name"),
            name="name",
            tags=(Tag.NAME,),
            type=str,
            data="Latitude",
            anns=(Tag.NAME,),
            orig=Quantity("Latitude", "deg"),
        ),
        Spec(
            path=Path("/lat/units"),
            name="units",
            tags=(Tag.UNITS,),
            type=str,
            data="deg",
            anns=(Tag.UNITS,),
            orig=Quantity("Latitude", "deg"),
        ),
        Spec(
            path=Path("/memo"),
            name="memo",
            tags=(),
            type=str,
            data="Observed in Tokyo",
            anns=(),
            orig=Weather([10, 20], [30, 40]),
        ),
    ]
)


def test_from_dataclass() -> None:
    assert from_dataclass(Weather([10, 20], [30, 40])) == specs
