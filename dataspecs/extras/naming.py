__all__ = ["Name", "name"]


# standard library
from collections.abc import Hashable
from dataclasses import dataclass, replace
from enum import auto
from typing import Annotated


# dependencies
from ..core.specs import Specs, TSpec
from ..core.typing import TagBase


# constants
class Tag(TagBase):
    NAME = auto()


@dataclass(frozen=True)
class Name:
    """Annotation for namer specs.

    Args:
        _name: New name of the data spec to be replaced.

    """

    _name: Annotated[Hashable, Tag.NAME]
    """New name of the data spec to be replaced."""


def name(specs: Specs[TSpec], /) -> Specs[TSpec]:
    """Replace data spec names by corresponding namer specs.

    Args:
        specs: Input data specs.

    Returns:
        Data specs whose names are replaced.

    Examples:
        ::

            from dataclasses import dataclass
            from dataspecs import Name, name, from_dataclass
            from typing import Annotated as Ann

            @dataclass
            class Weather:
                temp: Ann[float, Name("Ground temperature")]
                humid: Ann[float, Name("Relative humidity")]

            name(from_dataclass(Weather(20.0, 50.0)))

        ::

            Specs([
                Spec(
                    id=ID('/temp'),
                    name='Ground temperature',
                    tags=(),
                    type=<class 'float'>,
                    data=20.0,
                ),
                Spec(
                    id=ID('/temp/_name'),
                    name='_name',
                    tags=(<Tag.NAME: 1>,),
                    type=<class 'collections.abc.Hashable'>,
                    data='Ground temperature',
                ),
                Spec(
                    id=ID('/humid'),
                    name='Relative humidity',
                    tags=(),
                    type=<class 'float'>,
                    data=50.0,
                ),
                Spec(
                    id=ID('/humid/_name'),
                    name='_name',
                    tags=(<Tag.NAME: 1>,),
                    type=<class 'collections.abc.Hashable'>,
                    data='Relative humidity',
                ),
            ])

    """
    new = specs.copy()

    for spec in specs:
        options = specs[spec.id.children]

        if (name := options[Tag.NAME].unique) is not None:
            new = new.replace(spec, replace(spec, name=name.data))

    return new
