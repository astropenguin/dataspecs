__all__ = ["Name", "NameTag", "name"]


# standard library
from collections.abc import Hashable
from dataclasses import dataclass, replace
from enum import auto
from typing import Annotated


# dependencies
from ..core.specs import Specs, TSpec
from ..core.typing import TagBase


# constants
class NameTag(TagBase):
    NAME = auto()


@dataclass(frozen=True)
class Name:
    """Annotation for namer specs.

    Args:
        _name: New name of the data spec to be replaced.

    """

    _name: Annotated[Hashable, NameTag.NAME]
    """New name of the data spec to be replaced."""


def name(specs: Specs[TSpec], /, leave: bool = False) -> Specs[TSpec]:
    """Replace data spec names by corresponding namer specs.

    Args:
        specs: Input data specs.
        leave: Whether to leave the namer specs.

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
                    path=Path('/temp'),
                    name='Ground temperature', # <- named
                    tags=(),
                    type=<class 'float'>,
                    data=20.0,
                ),
                Spec(
                    path=Path('/humid'), # <- named
                    name='Relative humidity',
                    tags=(),
                    type=<class 'float'>,
                    data=50.0,
                ),
            ])

    """
    new = specs.copy()

    for spec in specs:
        options = specs[spec.path.children]

        if (name := options[NameTag.NAME].unique) is None:
            continue

        new = new.replace(spec, replace(spec, name=name.data))

        if not leave:
            new.remove(name)

    return new
