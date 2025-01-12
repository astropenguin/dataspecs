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

```python
from dataclasses import dataclass
from dataspecs import TagBase, from_dataclass
from enum import auto
from typing import Annotated as Ann
```

### Simple specifications

```python
class Tag(TagBase):
    ATTR = auto()
    DATA = auto()


@dataclass
class Weather:
    temp: Ann[list[float], Tag.DATA]
    humid: Ann[list[float], Tag.DATA]
    location: Ann[str, Tag.ATTR]


specs = from_dataclass(Weather([20.0, 25.0], [50.0, 55.0], "Tokyo"))
print(specs)
```
```
Specs([
    Spec(path=Path('/temp'), name='temp', tags=(<Tag.DATA: 2>,), type=list[float], data=[20.0, 25.0]),
    Spec(path=Path('/temp/0'), name='0', tags=(), type=<class 'float'>, data=None),
    Spec(path=Path('/humid'), name='humid', tags=(<Tag.DATA: 2>,), type=list[float], data=[50.0, 55.0]),
    Spec(path=Path('/humid/0'), name='0', tags=(), type=<class 'float'>, data=None),
    Spec(path=Path('/location'), name='location', tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='Tokyo'),
])
```

### Nested specifications

```python
class Tag(TagBase):
    ATTR = auto()
    DATA = auto()
    DTYPE = auto()
    NAME = auto()
    UNITS = auto()


@dataclass
class Meta:
    name: Ann[str, Tag.NAME]
    units: Ann[str, Tag.UNITS]


@dataclass
class Weather:
    temp: Ann[list[Ann[float, Tag.DTYPE]], Tag.DATA, Meta("Ground temperature", "K")]
    humid: Ann[list[Ann[float, Tag.DTYPE]], Tag.DATA, Meta("Relative humidity", "%")]
    location: Ann[str, Tag.ATTR]


specs = from_dataclass(Weather([20.0, 25.0], [50.0, 55.0], "Tokyo"))
print(specs)
```
```
Specs([
    Spec(path=Path('/temp'), name='temp', tags=(<Tag.DATA: 2>,), type=list[float], data=[20.0, 25.0]),
    Spec(path=Path('/temp/0'), name='0', tags=(<Tag.DTYPE: 3>,), type=<class 'float'>, data=None),
    Spec(path=Path('/temp/name'), name='name', tags=(<Tag.NAME: 4>,), type=<class 'str'>, data='Ground temperature'),
    Spec(path=Path('/temp/units'), name='units', tags=(<Tag.UNITS: 5>,), type=<class 'str'>, data='K'),
    Spec(path=Path('/humid'), name='humid', tags=(<Tag.DATA: 2>,), type=list[float], data=[50.0, 55.0]),
    Spec(path=Path('/humid/0'), name='0', tags=(<Tag.DTYPE: 3>,), type=<class 'float'>, data=None),
    Spec(path=Path('/humid/name'), name='name', tags=(<Tag.NAME: 4>,), type=<class 'str'>, data='Relative humidity'),
    Spec(path=Path('/humid/units'), name='units', tags=(<Tag.UNITS: 5>,), type=<class 'str'>, data='%'),
    Spec(path=Path('/location'), name='location', tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='Tokyo'),
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
    Spec(path=Path('/temp/name'), name='name', tags=(<Tag.NAME: 4>,), type=<class 'str'>, data='Ground temperature'),
    Spec(path=Path('/temp/units'), name='units', tags=(<Tag.UNITS: 5>,), type=<class 'str'>, data='K'),
    Spec(path=Path('/humid'), name='humid', tags=(<Tag.DATA: 2>,), type=list[float], data=[50.0, 55.0]),
    Spec(path=Path('/humid/0'), name='0', tags=(<Tag.DTYPE: 3>,), type=<class 'float'>, data=None),
    Spec(path=Path('/humid/name'), name='name', tags=(<Tag.NAME: 4>,), type=<class 'str'>, data='Relative humidity'),
    Spec(path=Path('/humid/units'), name='units', tags=(<Tag.UNITS: 5>,), type=<class 'str'>, data='%'),
    Spec(path=Path('/location'), name='location', tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='Tokyo'),
])
```

```python
specs[str]
```
```
Specs([
    Spec(path=Path('/temp/name'), name='name', tags=(<Tag.NAME: 4>,), type=<class 'str'>, data='Ground temperature'),
    Spec(path=Path('/temp/units'), name='units', tags=(<Tag.UNITS: 5>,), type=<class 'str'>, data='K'),
    Spec(path=Path('/humid/name'), name='name', tags=(<Tag.NAME: 4>,), type=<class 'str'>, data='Relative humidity'),
    Spec(path=Path('/humid/units'), name='units', tags=(<Tag.UNITS: 5>,), type=<class 'str'>, data='%'),
    Spec(path=Path('/location'), name='location', tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='Tokyo'),
])
```

```python
specs["/temp/[a-z]+"]
```
```
Specs([
    Spec(path=Path('/temp/name'), name='name', tags=(<Tag.NAME: 4>,), type=<class 'str'>, data='Ground temperature'),
    Spec(path=Path('/temp/units'), name='units', tags=(<Tag.UNITS: 5>,), type=<class 'str'>, data='K'),
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
        Spec(path=Path('/temp/name'), name='name', tags=(<Tag.NAME: 4>,), type=<class 'str'>, data='Ground temperature'),
        Spec(path=Path('/humid/name'), name='name', tags=(<Tag.NAME: 4>,), type=<class 'str'>, data='Relative humidity'),
    ]),
    Specs([
        Spec(path=Path('/temp/units'), name='units', tags=(<Tag.UNITS: 5>,), type=<class 'str'>, data='K'),
        Spec(path=Path('/humid/units'), name='units', tags=(<Tag.UNITS: 5>,), type=<class 'str'>, data='%'),
    ]),
    Specs([
        Spec(path=Path('/location'), name='location', tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='Tokyo'),
    ]),
]
```

## Advanced usage

### Formatting specifications

```python
from enum import auto
from dataclasses import dataclass
from dataspecs import TagBase, Format, from_dataclass, format
from typing import Annotated as Ann

class Tag(TagBase):
    ATTR = auto()

@dataclass
class Attrs:
    name: Ann[str, Tag.ATTR]
    units: Ann[str, Tag.ATTR]

@dataclass
class Weather:
    temp: Ann[list[float], Attrs("Temperature ({0})", "{0}")]
    units: Ann[str, Format("/temp/(name|units)")] = "degC"

format(from_dataclass(Weather([20.0, 25.0], "K")))
```
```
Specs([
    Spec(path=Path('/temp'), name='temp', tags=(), type=list[float], data=[20.0, 25.0]),
    Spec(path=Path('/temp/0'), name='0', tags=(), type=<class 'float'>, data=None),
    Spec(path=Path('/temp/name'), name='name', tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='Temperature (K)'), # <- formatted
    Spec(path=Path('/temp/units'), name='units', tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='K'), # <- formatted
    Spec(path=Path('/units'), name='units', tags=(), type=<class 'str'>, data='K'),
    Spec(path=Path('/units/_format_path'), name='_format_path', tags=(<FormatTag.PATH: 2>,), type=<class 'str'>, data='/temp/(name|units)'),
    Spec(path=Path('/units/_format_attr'), name='_format_attr', tags=(<FormatTag.ATTR: 1>,), type=typing.Literal['path', 'name', 'tags', 'type', 'data', 'anns', 'meta', 'orig'], data='data'),
    Spec(path=Path('/units/_format_skipif'), name='_format_skipif', tags=(<FormatTag.SKIPIF: 3>,), type=typing.Any, data=None),
])
```

### Naming specifications

```python
from dataclasses import dataclass
from dataspecs import Name, name, from_dataclass
from typing import Annotated as Ann

@dataclass
class Weather:
    temp: Ann[float, Name("Ground temperature")]
    humid: Ann[float, Name("Relative humidity")]

name(from_dataclass(Weather(20.0, 50.0)))
```
```
Specs([
    Spec(path=Path('/temp'), name='Ground temperature', tags=(), type=<class 'float'>, data=20.0), # <- named
    Spec(path=Path('/temp/_name'), name='_name', tags=(<NameTag.NAME: 1>,), type=<class 'collections.abc.Hashable'>, data='Ground temperature'),
    Spec(path=Path('/humid'), name='Relative humidity', tags=(), type=<class 'float'>, data=50.0), # <- named
    Spec(path=Path('/humid/_name'), name='_name', tags=(<NameTag.NAME: 1>,), type=<class 'collections.abc.Hashable'>, data='Relative humidity'),
])
```

### Replacing specifications

```python
from enum import auto
from dataclasses import dataclass
from dataspecs import Replace, TagBase, from_dataclass, replace
from typing import Annotated as Ann

class Tag(TagBase):
    ATTR = auto()
    DATA = auto()
    DTYPE = auto()

@dataclass
class Weather:
    temp: Ann[list[Ann[float, Tag.DTYPE]], Tag.DATA]
    humid: Ann[list[Ann[float, Tag.DTYPE]], Tag.DATA]
    dtype: Ann[type, Replace("/[a-z]+/0", "type")] = None

replace(from_dataclass(Weather([20.0, 25.0], [50.0, 55.0], int)))
```
```
Specs([
    Spec(path=Path('/temp'), name='temp', tags=(<Tag.DATA: 2>,), type=list[float], data=[20.0, 25.0]),
    Spec(path=Path('/temp/0'), name='0', tags=(<Tag.DTYPE: 3>,), type=<class 'int'>, data=None), # <- replaced
    Spec(path=Path('/humid'), name='humid', tags=(<Tag.DATA: 2>,), type=list[float], data=[50.0, 55.0]),
    Spec(path=Path('/humid/0'), name='0', tags=(<Tag.DTYPE: 3>,), type=<class 'int'>, data=None), # <- replaced
    Spec(path=Path('/dtype'), name='dtype', tags=(), type=<class 'type'>, data=<class 'int'>),
    Spec(path=Path('/dtype/_replace_path'), name='_replace_path', tags=(<ReplaceTag.PATH: 2>,), type=<class 'str'>, data='/[a-z]+/0'),
    Spec(path=Path('/dtype/_replace_attr'), name='_replace_attr', tags=(<ReplaceTag.ATTR: 1>,), type=typing.Literal['path', 'name', 'tags', 'type', 'data', 'anns', 'meta', 'orig'], data='type'),
    Spec(path=Path('/dtype/_replace_skipif'), name='_replace_skipif', tags=(<ReplaceTag.SKIPIF: 3>,), type=typing.Any, data=None),
])
```
