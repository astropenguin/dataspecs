__all__ = ["Format", "format"]


# standard library
from dataclasses import dataclass, replace
from enum import auto
from typing import Annotated, Any


# dependencies
from ..core.specs import SpecAttr, Specs, TSpec
from ..core.typing import StrPath, TagBase


# constants
class Tag(TagBase):
    ID = auto()
    OF = auto()
    SKIPIF = auto()


@dataclass(frozen=True)
class Format:
    """Annotation for formatter specs.

    Args:
        _format_id: ID of data spec(s) to be formatted.
        _format_of: Name of data spec attribute to be formatted.
        _format_skipif: Sentinel value for which formatting is skipped.

    """

    _format_id: Annotated[StrPath, Tag.ID]
    """ID of data spec(s) to be formatted."""

    _format_of: Annotated[SpecAttr, Tag.OF] = "data"
    """Name of data spec attribute to be formatted."""

    _format_skipif: Annotated[Any, Tag.SKIPIF] = None
    """Sentinel value for which formatting is skipped."""


def format(specs: Specs[TSpec], /) -> Specs[TSpec]:
    """Format data spec attributes by formatter specs.

    Args:
        specs: Input data specs.

    Returns:
        Data specs whose attributes are formatted.

    Examples:
        ::

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

        ::

            Specs([
                Spec(
                    id=ID('/temp'),
                    tags=(),
                    type=list[float],
                    data=[20.0, 25.0],
                ),
                Spec(
                    id=ID('/temp/0'),
                    tags=(),
                    type=<class 'float'>,
                    data=None,
                ),
                Spec(
                    id=ID('/temp/name'),
                    tags=(<Tag.ATTR: 1>,),
                    type=<class 'str'>,
                    data='Temperature (K)', # <- formatted
                ),
                Spec(
                    id=ID('/temp/units'),
                    tags=(<Tag.ATTR: 1>,),
                    type=<class 'str'>, data='K', # <- formatted
                ),
                Spec(
                    id=ID('/units'),
                    tags=(),
                    type=<class 'str'>,
                    data='K',
                ),
                Spec(
                    id=ID('/units/_format_id'),
                    tags=(<Tag.ID: 1>,),
                    type=<class 'str'>,
                    data='/temp/attrs/(name|units)',
                ),
                Spec(
                    id=ID('/units/_format_of'),
                    tags=(<Tag.OF: 2>,),
                    type=<class 'str'>,
                    data='data',
                ),
                Spec(
                    id=ID('/units/_format_skipif'),
                    tags=(<Tag.SKIPIF: 3>,),
                    type=typing.Any,
                    data=None,
                ),
            ])

    """
    new = specs.copy()

    for spec in specs:
        for options in specs[spec.id.children].groupby("origin", method="id"):
            if (
                (id := options[Tag.ID].unique) is None
                or (of := options[Tag.OF].unique) is None
                or (skipif := options[Tag.SKIPIF].unique) is None
            ):
                continue

            if spec.data == skipif.data:
                continue

            for target in new[id[str].data]:
                attr: str = getattr(target, of[str].data)
                changes = {of[str].data: attr.format(spec.data)}
                updated = replace(target, **changes)  # type: ignore
                new = new.replace(target, updated)

    return new
