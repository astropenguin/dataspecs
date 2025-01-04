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

## Usage

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
specs
```
```
Specs([
    Spec(id=ID('/'), tags=(), type=<class '__main__.Weather'>, data=Weather(temp=[20.0, 25.0], humid=[50.0, 55.0], location='Tokyo')),
    Spec(id=ID('/temp'), tags=(<Tag.DATA: 2>,), type=list[float], data=[20.0, 25.0]),
    Spec(id=ID('/temp/0'), tags=(), type=<class 'float'>, data=None),
    Spec(id=ID('/humid'), tags=(<Tag.DATA: 2>,), type=list[float], data=[50.0, 55.0]),
    Spec(id=ID('/humid/0'), tags=(), type=<class 'float'>, data=None),
    Spec(id=ID('/location'), tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='Tokyo'),
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
specs
```
```
Specs([
    Spec(id=ID('/temp'), tags=(<Tag.DATA: 2>,), type=list[float], data=[20.0, 25.0]),
    Spec(id=ID('/temp/0'), tags=(<Tag.DTYPE: 3>,), type=<class 'float'>, data=None),
    Spec(id=ID('/temp/name'), tags=(<Tag.NAME: 4>,), type=<class 'str'>, data='Ground temperature'),
    Spec(id=ID('/temp/units'), tags=(<Tag.UNITS: 5>,), type=<class 'str'>, data='K'),
    Spec(id=ID('/humid'), tags=(<Tag.DATA: 2>,), type=list[float], data=[50.0, 55.0]),
    Spec(id=ID('/humid/0'), tags=(<Tag.DTYPE: 3>,), type=<class 'float'>, data=None),
    Spec(id=ID('/humid/name'), tags=(<Tag.NAME: 4>,), type=<class 'str'>, data='Relative humidity'),
    Spec(id=ID('/humid/units'), tags=(<Tag.UNITS: 5>,), type=<class 'str'>, data='%'),
    Spec(id=ID('/location'), tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='Tokyo'),
])
```

### Selecting specifications

```python
specs[Tag.DATA]
```
```
Specs([
    Spec(id=ID('/temp'), tags=(<Tag.DATA: 2>,), type=list[float], data=[20.0, 25.0]),
    Spec(id=ID('/humid'), tags=(<Tag.DATA: 2>,), type=list[float], data=[50.0, 55.0]),
])
```

```python
specs[Tag]
```
```
Specs([
    Spec(id=ID('/temp'), tags=(<Tag.DATA: 2>,), type=list[float], data=[20.0, 25.0]),
    Spec(id=ID('/temp/0'), tags=(<Tag.DTYPE: 3>,), type=<class 'float'>, data=None),
    Spec(id=ID('/temp/name'), tags=(<Tag.NAME: 4>,), type=<class 'str'>, data='Ground temperature'),
    Spec(id=ID('/temp/units'), tags=(<Tag.UNITS: 5>,), type=<class 'str'>, data='K'),
    Spec(id=ID('/humid'), tags=(<Tag.DATA: 2>,), type=list[float], data=[50.0, 55.0]),
    Spec(id=ID('/humid/0'), tags=(<Tag.DTYPE: 3>,), type=<class 'float'>, data=None),
    Spec(id=ID('/humid/name'), tags=(<Tag.NAME: 4>,), type=<class 'str'>, data='Relative humidity'),
    Spec(id=ID('/humid/units'), tags=(<Tag.UNITS: 5>,), type=<class 'str'>, data='%'),
    Spec(id=ID('/location'), tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='Tokyo'),
])
```

```python
specs[str]
```
```
Specs([
    Spec(id=ID('/temp/name'), tags=(<Tag.NAME: 4>,), type=<class 'str'>, data='Ground temperature'),
    Spec(id=ID('/temp/units'), tags=(<Tag.UNITS: 5>,), type=<class 'str'>, data='K'),
    Spec(id=ID('/humid/name'), tags=(<Tag.NAME: 4>,), type=<class 'str'>, data='Relative humidity'),
    Spec(id=ID('/humid/units'), tags=(<Tag.UNITS: 5>,), type=<class 'str'>, data='%'),
    Spec(id=ID('/location'), tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='Tokyo'),
])
```

```python
specs["/temp/[a-z]+"]
```
```
Specs([
    Spec(id=ID('/temp/name'), tags=(<Tag.NAME: 4>,), type=<class 'str'>, data='Ground temperature'),
    Spec(id=ID('/temp/units'), tags=(<Tag.UNITS: 5>,), type=<class 'str'>, data='K'),
])
```

### Grouping specifications

```python
specs.groupby("tags")
```
```
[
    Specs([
        Spec(id=ID('/temp'), tags=(<Tag.DATA: 2>,), type=list[float], data=[20.0, 25.0]),
        Spec(id=ID('/humid'), tags=(<Tag.DATA: 2>,), type=list[float], data=[50.0, 55.0]),
    ]),
    Specs([
        Spec(id=ID('/temp/0'), tags=(<Tag.DTYPE: 3>,), type=<class 'float'>, data=None),
        Spec(id=ID('/humid/0'), tags=(<Tag.DTYPE: 3>,), type=<class 'float'>, data=None),
    ]),
    Specs([
        Spec(id=ID('/temp/name'), tags=(<Tag.NAME: 4>,), type=<class 'str'>, data='Ground temperature'),
        Spec(id=ID('/humid/name'), tags=(<Tag.NAME: 4>,), type=<class 'str'>, data='Relative humidity'),
    ]),
    Specs([
        Spec(id=ID('/temp/units'), tags=(<Tag.UNITS: 5>,), type=<class 'str'>, data='K'),
        Spec(id=ID('/humid/units'), tags=(<Tag.UNITS: 5>,), type=<class 'str'>, data='%'),
    ]),
    Specs([
        Spec(id=ID('/location'), tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='Tokyo')
    ]),
]
```

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
    Spec(id=ID('/temp'), tags=(), type=list[float], data=[20.0, 25.0]),
    Spec(id=ID('/temp/0'), tags=(), type=<class 'float'>, data=None),
    Spec(id=ID('/temp/name'), tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='Temperature (K)'), # <- formatted
    Spec(id=ID('/temp/units'), tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='K'), # <- formatted
    Spec(id=ID('/units'), tags=(), type=<class 'str'>, data='K'),
    Spec(id=ID('/units/_format_id'), tags=(<Tag.ID: 1>,), type=<class 'str'>, data='/temp/(name|units)'),
    Spec(id=ID('/units/_format_of'), tags=(<Tag.OF: 2>,), type=<class 'str'>, data='data'),
    Spec(id=ID('/units/_format_skipif'), tags=(<Tag.SKIPIF: 3>,), type=typing.Any, data=None),
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
    Spec(id=ID('/temp'), tags=(<Tag.DATA: 2>,), type=list[float], data=[20.0, 25.0]),
    Spec(id=ID('/temp/0'), tags=(<Tag.DTYPE: 3>,), type=<class 'int'>, data=None), # <- replaced
    Spec(id=ID('/humid'), tags=(<Tag.DATA: 2>,), type=list[float], data=[50.0, 55.0]),
    Spec(id=ID('/humid/0'), tags=(<Tag.DTYPE: 3>,), type=<class 'int'>, data=None), # <- replaced
    Spec(id=ID('/dtype'), tags=(), type=<class 'type'>, data=<class 'int'>),
    Spec(id=ID('/dtype/_replace_id'), tags=(<Tag.ID: 1>,), type=<class 'str'>, data='/[a-z]+/0'),
    Spec(id=ID('/dtype/_replace_of'), tags=(<Tag.OF: 2>,), type=<class 'str'>, data='type'),
    Spec(id=ID('/dtype/_replace_skipif'), tags=(<Tag.SKIPIF: 3>,), type=typing.Any, data=None),
])
```
