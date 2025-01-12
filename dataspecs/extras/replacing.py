__all__ = ["Replace", "replace"]


# standard library
from dataclasses import dataclass, replace as replace_
from enum import auto
from typing import Annotated, Any


# dependencies
from ..core.specs import SpecAttr, Specs, TSpec
from ..core.typing import StrPath, TagBase


# constants
class Tag(TagBase):
    PATH = auto()
    OF = auto()
    SKIPIF = auto()


@dataclass(frozen=True)
class Replace:
    """Annotation for replacer specs.

    Args:
        _replace_path: Path of data spec(s) to be replaced.
        _replace_of: Name of data spec attribute to be replaced.
        _replace_skipif: Sentinel value for which replacing is skipped.

    """

    _replace_path: Annotated[StrPath, Tag.PATH]
    """Path of data spec(s) to be replaced."""

    _replace_of: Annotated[SpecAttr, Tag.OF] = "data"
    """Name of data spec attribute to be replaced."""

    _replace_skipif: Annotated[Any, Tag.SKIPIF] = None
    """Sentinel value for which replacing is skipped."""


def replace(specs: Specs[TSpec], /) -> Specs[TSpec]:
    """Replace data spec attributes by replacer specs.

    Args:
        specs: Input data specs.

    Returns:
        Data specs whose attributes are replaced.

    Examples:
        ::

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

        ::

            Specs([
                Spec(
                    path=Path('/temp'),
                    tags=(<Tag.DATA: 2>,),
                    type=list[float],
                    data=[20.0, 25.0],
                ),
                Spec(
                    path=Path('/temp/0'),
                    tags=(<Tag.DTYPE: 3>,),
                    type=<class 'int'>, # <- replaced
                    data=None,
                ),
                Spec(
                    path=Path('/humid'),
                    tags=(<Tag.DATA: 2>,),
                    type=list[float],
                    data=[50.0, 55.0],
                ),
                Spec(
                    path=Path('/humid/0'),
                    tags=(<Tag.DTYPE: 3>,),
                    type=<class 'int'>, # <- replaced
                    data=None,
                ),
                Spec(
                    path=Path('/dtype'),
                    tags=(),
                    type=<class 'type'>,
                    data=<class 'int'>,
                ),
                Spec(
                    path=Path('/dtype/_replace_path'),
                    tags=(<Tag.PATH: 1>,),
                    type=<class 'str'>,
                    data='/[a-z]+/0',
                ),
                Spec(
                    path=Path('/dtype/_replace_of'),
                    tags=(<Tag.OF: 2>,),
                    type=<class 'str'>,
                    data='type',
                ),
                Spec(
                    path=Path('/dtype/_replace_skipif'),
                    tags=(<Tag.SKIPIF: 3>,),
                    type=typing.Any,
                    data=None,
                ),
            ])

    """
    new = specs.copy()

    for spec in specs:
        for options in specs[spec.path.children].groupby("orig", method="id"):
            if (
                (path := options[Tag.PATH].unique) is None
                or (of := options[Tag.OF].unique) is None
                or (skipif := options[Tag.SKIPIF].unique) is None
            ):
                continue

            if spec.data == skipif.data:
                continue

            for target in new[path[str].data]:
                changes = {of[str].data: spec.data}
                updated = replace_(target, **changes)  # type: ignore
                new = new.replace(target, updated)

    return new
