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


simple_specs = from_dataclass(Weather([20.0, 25.0], [50.0, 55.0], "Tokyo"))
simple_specs
```
```python
Specs([Spec(id=ID('/'), type=<class '__main__.Weather'>, data=Weather(temp=[20.0, 25.0], humid=[50.0, 55.0], location='Tokyo'), tags=(), meta=()),
       Spec(id=ID('/temp'), type=list[float], data=[20.0, 25.0], tags=(<Tag.DATA: 2>,), meta=()),
       Spec(id=ID('/temp/0'), type=<class 'float'>, data=None, tags=(), meta=()),
       Spec(id=ID('/humid'), type=list[float], data=[50.0, 55.0], tags=(<Tag.DATA: 2>,), meta=()),
       Spec(id=ID('/humid/0'), type=<class 'float'>, data=None, tags=(), meta=()),
       Spec(id=ID('/location'), type=<class 'str'>, data='Tokyo', tags=(<Tag.ATTR: 1>,), meta=())])
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


nested_specs = from_dataclass(Weather([20.0, 25.0], [50.0, 55.0], "Tokyo"))
nested_specs
```
```python
Specs([Spec(id=ID('/'), type=<class '__main__.Weather'>, data=Weather(temp=[20.0, 25.0], humid=[50.0, 55.0], location='Tokyo'), tags=(), meta=()),
       Spec(id=ID('/temp'), type=list[float], data=[20.0, 25.0], tags=(<Tag.DATA: 2>,), meta=()),
       Spec(id=ID('/temp/0'), type=<class 'float'>, data=None, tags=(<Tag.DTYPE: 3>,), meta=()),
       Spec(id=ID('/temp/meta'), type=<class '__main__.Meta'>, data=Meta(name='Ground temperature', units='K'), tags=(), meta=()),
       Spec(id=ID('/temp/meta/name'), type=<class 'str'>, data='Ground temperature', tags=(<Tag.NAME: 4>,), meta=()),
       Spec(id=ID('/temp/meta/units'), type=<class 'str'>, data='K', tags=(<Tag.UNITS: 5>,), meta=()),
       Spec(id=ID('/humid'), type=list[float], data=[50.0, 55.0], tags=(<Tag.DATA: 2>,), meta=()),
       Spec(id=ID('/humid/0'), type=<class 'float'>, data=None, tags=(<Tag.DTYPE: 3>,), meta=()),
       Spec(id=ID('/humid/meta'), type=<class '__main__.Meta'>, data=Meta(name='Relative humidity', units='%'), tags=(), meta=()),
       Spec(id=ID('/humid/meta/name'), type=<class 'str'>, data='Relative humidity', tags=(<Tag.NAME: 4>,), meta=()),
       Spec(id=ID('/humid/meta/units'), type=<class 'str'>, data='%', tags=(<Tag.UNITS: 5>,), meta=()),
       Spec(id=ID('/location'), type=<class 'str'>, data='Tokyo', tags=(<Tag.ATTR: 1>,), meta=())])
```

### Selecting specifications

```python
nested_specs[Tag.DATA]
```
```python
Specs([Spec(id=ID('/temp'), type=list[float], data=[20.0, 25.0], tags=(<Tag.DATA: 2>,), meta=()),
       Spec(id=ID('/humid'), type=list[float], data=[50.0, 55.0], tags=(<Tag.DATA: 2>,), meta=())])
```

```python
nested_specs[Tag]
```
```python
Specs([Spec(id=ID('/temp'), type=list[float], data=[20.0, 25.0], tags=(<Tag.DATA: 2>,), meta=()),
       Spec(id=ID('/temp/0'), type=<class 'float'>, data=None, tags=(<Tag.DTYPE: 3>,), meta=()),
       Spec(id=ID('/temp/meta/name'), type=<class 'str'>, data='Ground temperature', tags=(<Tag.NAME: 4>,), meta=()),
       Spec(id=ID('/temp/meta/units'), type=<class 'str'>, data='K', tags=(<Tag.UNITS: 5>,), meta=()),
       Spec(id=ID('/humid'), type=list[float], data=[50.0, 55.0], tags=(<Tag.DATA: 2>,), meta=()),
       Spec(id=ID('/humid/0'), type=<class 'float'>, data=None, tags=(<Tag.DTYPE: 3>,), meta=()),
       Spec(id=ID('/humid/meta/name'), type=<class 'str'>, data='Relative humidity', tags=(<Tag.NAME: 4>,), meta=()),
       Spec(id=ID('/humid/meta/units'), type=<class 'str'>, data='%', tags=(<Tag.UNITS: 5>,), meta=()),
       Spec(id=ID('/location'), type=<class 'str'>, data='Tokyo', tags=(<Tag.ATTR: 1>,), meta=())])
```

```python
nested_specs[str]
```
```python
Specs([Spec(id=ID('/temp/meta/name'), type=<class 'str'>, data='Ground temperature', tags=(<Tag.NAME: 4>,), meta=()),
       Spec(id=ID('/temp/meta/units'), type=<class 'str'>, data='K', tags=(<Tag.UNITS: 5>,), meta=()),
       Spec(id=ID('/humid/meta/name'), type=<class 'str'>, data='Relative humidity', tags=(<Tag.NAME: 4>,), meta=()),
       Spec(id=ID('/humid/meta/units'), type=<class 'str'>, data='%', tags=(<Tag.UNITS: 5>,), meta=()),
       Spec(id=ID('/location'), type=<class 'str'>, data='Tokyo', tags=(<Tag.ATTR: 1>,), meta=())])
```

```python
nested_specs["/temp/meta/[a-z]+"]
```
```python
Specs([Spec(id=ID('/temp/meta/name'), type=<class 'str'>, data='Ground temperature', tags=(<Tag.NAME: 4>,), meta=()),
       Spec(id=ID('/temp/meta/units'), type=<class 'str'>, data='K', tags=(<Tag.UNITS: 5>,), meta=())])
```
