# dataspecs

[![Release](https://img.shields.io/pypi/v/dataspecs?label=Release&color=cornflowerblue&style=flat-square)](https://pypi.org/project/dataspecs/)
[![Python](https://img.shields.io/pypi/pyversions/dataspecs?label=Python&color=cornflowerblue&style=flat-square)](https://pypi.org/project/dataspecs/)
[![Downloads](https://img.shields.io/pypi/dm/dataspecs?label=Downloads&color=cornflowerblue&style=flat-square)](https://pepy.tech/project/dataspecs)
[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.10652375-cornflowerblue?style=flat-square)](https://doi.org/10.5281/zenodo.10652375)
[![Tests](https://img.shields.io/github/actions/workflow/status/astropenguin/dataspecs/tests.yaml?label=Tests&style=flat-square)](https://github.com/astropenguin/dataspecs/actions)

Data specifications by data classes

## Installation

```shell
pip install dataspecs
```

## Basic usage

### Common imports and tags

```python
from dataclasses import dataclass
from dataspecs import TagBase, from_dataclass
from enum import auto
from typing import Annotated as Ann

class Tag(TagBase):
    ATTR = auto()
    DATA = auto()
    DTYPE = auto()
```

### Simple specifications

```python
@dataclass
class Weather:
    temp: list[float]
    humid: list[float]
    location: str

specs = from_dataclass(Weather([20.0, 25.0], [50.0, 55.0], "Tokyo"))
print(specs)
```
```
Specs([
    Spec(path=Path('/temp'), name='temp', tags=(), type=list[float], data=[20.0, 25.0]),
    Spec(path=Path('/temp/0'), name='0', tags=(), type=<class 'float'>, data=None),
    Spec(path=Path('/humid'), name='humid', tags=(), type=list[float], data=[50.0, 55.0]),
    Spec(path=Path('/humid/0'), name='0', tags=(), type=<class 'float'>, data=None),
    Spec(path=Path('/location'), name='location', tags=(), type=<class 'str'>, data='Tokyo'),
])
```

### Simple specifications with tags

```python
@dataclass
class Weather:
    temp: Ann[list[float], Tag.DATA]
    humid: Ann[list[float], Tag.DATA]
    location: str

specs = from_dataclass(Weather([20.0, 25.0], [50.0, 55.0], "Tokyo"))
print(specs)
```
```
Specs([
    Spec(path=Path('/temp'), name='temp', tags=(<Tag.DATA: 2>,), type=list[float], data=[20.0, 25.0]),
    Spec(path=Path('/temp/0'), name='0', tags=(), type=<class 'float'>, data=None),
    Spec(path=Path('/humid'), name='humid', tags=(<Tag.DATA: 2>,), type=list[float], data=[50.0, 55.0]),
    Spec(path=Path('/humid/0'), name='0', tags=(), type=<class 'float'>, data=None),
    Spec(path=Path('/location'), name='location', tags=(), type=<class 'str'>, data='Tokyo'),
])
```

### Nested specifications (with tags)

```python
@dataclass
class Meta:
    units: Ann[str, Tag.ATTR]

@dataclass
class Weather:
    temp: Ann[list[Ann[float, Tag.DTYPE]], Tag.DATA, Meta("degC")]
    humid: Ann[list[Ann[float, Tag.DTYPE]], Tag.DATA, Meta("%")]
    location: str

specs = from_dataclass(Weather([20.0, 25.0], [50.0, 55.0], "Tokyo"))
print(specs)
```
```
Specs([
    Spec(path=Path('/temp'), name='temp', tags=(<Tag.DATA: 2>,), type=list[float], data=[20.0, 25.0]),
    Spec(path=Path('/temp/0'), name='0', tags=(<Tag.DTYPE: 3>,), type=<class 'float'>, data=None),
    Spec(path=Path('/temp/units'), name='units', tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='degC'),
    Spec(path=Path('/humid'), name='humid', tags=(<Tag.DATA: 2>,), type=list[float], data=[50.0, 55.0]),
    Spec(path=Path('/humid/0'), name='0', tags=(<Tag.DTYPE: 3>,), type=<class 'float'>, data=None),
    Spec(path=Path('/humid/units'), name='units', tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='%'),
    Spec(path=Path('/location'), name='location', tags=(), type=<class 'str'>, data='Tokyo'),
])
```

### Selecting specifications

```python
specs[Tag.DATA]
```
```
Specs([
    Spec(path=Path('/temp'), name='temp', tags=(<Tag.DATA: 2>,), type=list[float], data=[20.0, 25.0]),
    Spec(path=Path('/humid'), name='humid', tags=(<Tag.DATA: 2>,), type=list[float], data=[50.0, 55.0]),
])
```

```python
specs[Tag]
```
```
Specs([
    Spec(path=Path('/temp'), name='temp', tags=(<Tag.DATA: 2>,), type=list[float], data=[20.0, 25.0]),
    Spec(path=Path('/temp/0'), name='0', tags=(<Tag.DTYPE: 3>,), type=<class 'float'>, data=None),
    Spec(path=Path('/temp/units'), name='units', tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='degC'),
    Spec(path=Path('/humid'), name='humid', tags=(<Tag.DATA: 2>,), type=list[float], data=[50.0, 55.0]),
    Spec(path=Path('/humid/0'), name='0', tags=(<Tag.DTYPE: 3>,), type=<class 'float'>, data=None),
    Spec(path=Path('/humid/units'), name='units', tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='%'),
])
```

```python
specs[str]
```
```
Specs([
    Spec(path=Path('/temp/units'), name='units', tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='degC'),
    Spec(path=Path('/humid/units'), name='units', tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='%'),
    Spec(path=Path('/location'), name='location', tags=(), type=<class 'str'>, data='Tokyo'),
])
```

```python
specs["/temp/[a-z]+"]
```
```
Specs([
    Spec(path=Path('/temp/units'), name='units', tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='degC'),
])
```

### Grouping specifications

```python
specs.groupby("tags")
```
```
[
    Specs([
        Spec(path=Path('/temp'), name='temp', tags=(<Tag.DATA: 2>,), type=list[float], data=[20.0, 25.0]),
        Spec(path=Path('/humid'), name='humid', tags=(<Tag.DATA: 2>,), type=list[float], data=[50.0, 55.0]),
    ]),
    Specs([
        Spec(path=Path('/temp/0'), name='0', tags=(<Tag.DTYPE: 3>,), type=<class 'float'>, data=None),
        Spec(path=Path('/humid/0'), name='0', tags=(<Tag.DTYPE: 3>,), type=<class 'float'>, data=None),
    ]),
    Specs([
        Spec(path=Path('/temp/units'), name='units', tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='degC'),
        Spec(path=Path('/humid/units'), name='units', tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='%'),
    ]),
    Specs([
        Spec(path=Path('/location'), name='location', tags=(), type=<class 'str'>, data='Tokyo'),
    ]),
]
```

## Advanced usage

### Formatting specifications

```python
from dataspecs import Format, format

@dataclass
class Meta:
    units: Ann[str, Tag.ATTR]

@dataclass
class Weather:
    temp: Ann[float, Meta("{0}")]
    humid: Ann[float, Meta("{0}")]
    temp_units: Ann[str, Format("/temp/units")]
    humid_units: Ann[str, Format("/humid/units")]

format(from_dataclass(Weather(20.0, 50.0, "degC", "%")))
```
```
Specs([
    Spec(path=Path('/temp'), name='temp', tags=(), type=<class 'float'>, data=20.0),
    Spec(path=Path('/temp/units'), name='units', tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='degC'), # <- data formatted
    Spec(path=Path('/humid'), name='humid', tags=(), type=<class 'float'>, data=50.0),
    Spec(path=Path('/humid/units'), name='units', tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='%'), # <- data formatted
    Spec(path=Path('/temp_units'), name='temp_units', tags=(), type=<class 'str'>, data='degC'),
    Spec(path=Path('/humid_units'), name='humid_units', tags=(), type=<class 'str'>, data='%'),
])
```

### Naming specifications

```python
from dataspecs import Name, name

@dataclass
class Weather:
    temp: Ann[float, Name("Ground temperature")]
    humid: Ann[float, Name("Relative humidity")]

name(from_dataclass(Weather(20.0, 50.0)))
```
```
Specs([
    Spec(path=Path('/temp'), name='Ground temperature', tags=(), type=<class 'float'>, data=20.0), # <- name replaced
    Spec(path=Path('/humid'), name='Relative humidity', tags=(), type=<class 'float'>, data=50.0), # <- name replaced
])
```

### Replacing specifications

```python
from dataspecs import Replace, replace

@dataclass
class Weather:
    temp: Ann[list[Ann[float, Tag.DTYPE]], Tag.DATA]
    humid: Ann[list[Ann[float, Tag.DTYPE]], Tag.DATA]
    dtype: Ann[type, Replace("/[a-z]+/0", "type")]

replace(from_dataclass(Weather([20.0, 25.0], [50.0, 55.0], int)))
```
```
Specs([
    Spec(path=Path('/temp'), name='temp', tags=(<Tag.DATA: 2>,), type=list[float], data=[20.0, 25.0]),
    Spec(path=Path('/temp/0'), name='0', tags=(<Tag.DTYPE: 3>,), type=<class 'int'>, data=None), # <- type replaced
    Spec(path=Path('/humid'), name='humid', tags=(<Tag.DATA: 2>,), type=list[float], data=[50.0, 55.0]),
    Spec(path=Path('/humid/0'), name='0', tags=(<Tag.DTYPE: 3>,), type=<class 'int'>, data=None), # <- type replaced
    Spec(path=Path('/dtype'), name='dtype', tags=(), type=<class 'type'>, data=<class 'int'>),
])
```

## Specification rules

### First union type as representative type

```python
@dataclass
class Weather:
    temp: list[int | float] | (int | float)

from_dataclass(Weather(0.0))
```
```
Specs([
    Spec(path=Path('/temp'), name='temp', tags=(), type=list[int | float], data=0.0),
    Spec(path=Path('/temp/0'), name='0', tags=(), type=<class 'int'>, data=None),
])
```
