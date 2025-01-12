__all__ = ["Format", "format"]


# standard library
from dataclasses import dataclass, replace
from enum import auto
from typing import Annotated, Any


# dependencies
from ..core.specs import SpecAttr, Specs, TSpec
from ..core.typing import StrPath, TagBase


# constants
class FormatTag(TagBase):
    ATTR = auto()
    PATH = auto()
    SKIPIF = auto()


@dataclass(frozen=True)
class Format:
    """Annotation for formatter specs.

    Args:
        _format_path: Path of data spec(s) to be formatted.
        _format_attr: Name of data spec attribute to be formatted.
        _format_skipif: Sentinel value for which formatting is skipped.

    """

    _format_path: Annotated[StrPath, FormatTag.PATH]
    """Path of data spec(s) to be formatted."""

    _format_attr: Annotated[SpecAttr, FormatTag.ATTR] = "data"
    """Name of data spec attribute to be formatted."""

    _format_skipif: Annotated[Any, FormatTag.SKIPIF] = None
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
                    path=Path('/temp'),
                    tags=(),
                    type=list[float],
                    data=[20.0, 25.0],
                ),
                Spec(
                    path=Path('/temp/0'),
                    tags=(),
                    type=<class 'float'>,
                    data=None,
                ),
                Spec(
                    path=Path('/temp/name'),
                    tags=(<Tag.ATTR: 1>,),
                    type=<class 'str'>,
                    data='Temperature (K)', # <- formatted
                ),
                Spec(
                    path=Path('/temp/units'),
                    tags=(<Tag.ATTR: 1>,),
                    type=<class 'str'>, data='K', # <- formatted
                ),
                Spec(
                    path=Path('/units'),
                    tags=(),
                    type=<class 'str'>,
                    data='K',
                ),
                Spec(
                    path=Path('/units/_format_path'),
                    tags=(<FormatTag.PATH: 1>,),
                    type=<class 'str'>,
                    data='/temp/attrs/(name|units)',
                ),
                Spec(
                    path=Path('/units/_format_attr'),
                    tags=(<FormatTag.ATTR: 2>,),
                    type=<class 'str'>,
                    data='data',
                ),
                Spec(
                    path=Path('/units/_format_skipif'),
                    tags=(<FormatTag.SKIPIF: 3>,),
                    type=typing.Any,
                    data=None,
                ),
            ])

    """
    new = specs.copy()

    for spec in specs:
        for options in specs[spec.path.children].groupby("orig", method="id"):
            if (
                (path := options[FormatTag.PATH].unique) is None
                or (attr := options[FormatTag.ATTR].unique) is None
                or (skipif := options[FormatTag.SKIPIF].unique) is None
            ):
                continue

            if spec.data == skipif.data:
                continue

            for target in new[path[str].data]:
                string: str = getattr(target, attr[str].data)
                changes = {attr[str].data: string.format(spec.data)}
                updated = replace(target, **changes)
                new = new.replace(target, updated)

    return new
