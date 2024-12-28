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
Specs([Spec(id=ID('/temp'), tags=(<Tag.DATA: 2>,), type=list[float], data=[20.0, 25.0]),
       Spec(id=ID('/humid'), tags=(<Tag.DATA: 2>,), type=list[float], data=[50.0, 55.0]),
       Spec(id=ID('/location'), tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='Tokyo')])
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
Specs([Spec(id=ID('/temp'), tags=(<Tag.DATA: 2>,), type=list[float], data=[20.0, 25.0]),
       Spec(id=ID('/temp/0'), tags=(<Tag.DTYPE: 3>,), type=<class 'float'>, data=None),
       Spec(id=ID('/temp/name'), tags=(<Tag.NAME: 4>,), type=<class 'str'>, data='Ground temperature'),
       Spec(id=ID('/temp/units'), tags=(<Tag.UNITS: 5>,), type=<class 'str'>, data='K'),
       Spec(id=ID('/humid'), tags=(<Tag.DATA: 2>,), type=list[float], data=[50.0, 55.0]),
       Spec(id=ID('/humid/0'), tags=(<Tag.DTYPE: 3>,), type=<class 'float'>, data=None),
       Spec(id=ID('/humid/name'), tags=(<Tag.NAME: 4>,), type=<class 'str'>, data='Relative humidity'),
       Spec(id=ID('/humid/units'), tags=(<Tag.UNITS: 5>,), type=<class 'str'>, data='%'),
       Spec(id=ID('/location'), tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='Tokyo')])
```

### Selecting specifications

```python
nested_specs[Tag.DATA]
```
```python
Specs([Spec(id=ID('/temp'), tags=(<Tag.DATA: 2>,), type=list[float], data=[20.0, 25.0]),
       Spec(id=ID('/humid'), tags=(<Tag.DATA: 2>,), type=list[float], data=[50.0, 55.0])])
```

```python
nested_specs["/temp/[a-z]+"]
```
```python
Specs([Spec(id=ID('/temp/name'), tags=(<Tag.NAME: 4>,), type=<class 'str'>, data='Ground temperature'),
       Spec(id=ID('/temp/units'), tags=(<Tag.UNITS: 5>,), type=<class 'str'>, data='K')])
```

### Grouping specifications

```python
nested_specs.groups()
```
```python
[Specs([Spec(id=ID('/temp'), tags=(<Tag.DATA: 2>,), type=list[float], data=[20.0, 25.0]),
        Spec(id=ID('/temp/0'), tags=(<Tag.DTYPE: 3>,), type=<class 'float'>, data=None),
        Spec(id=ID('/temp/name'), tags=(<Tag.NAME: 4>,), type=<class 'str'>, data='Ground temperature'),
        Spec(id=ID('/temp/units'), tags=(<Tag.UNITS: 5>,), type=<class 'str'>, data='K')]),
 Specs([Spec(id=ID('/humid'), tags=(<Tag.DATA: 2>,), type=list[float], data=[50.0, 55.0]),
        Spec(id=ID('/humid/0'), tags=(<Tag.DTYPE: 3>,), type=<class 'float'>, data=None),
        Spec(id=ID('/humid/name'), tags=(<Tag.NAME: 4>,), type=<class 'str'>, data='Relative humidity'),
        Spec(id=ID('/humid/units'), tags=(<Tag.UNITS: 5>,), type=<class 'str'>, data='%')]),
 Specs([Spec(id=ID('/location'), tags=(<Tag.ATTR: 1>,), type=<class 'str'>, data='Tokyo')])]
```
