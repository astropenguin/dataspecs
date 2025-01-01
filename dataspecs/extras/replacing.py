__all__ = ["Replace", "replace"]


# standard library
from dataclasses import dataclass, replace as replace_
from enum import auto
from typing import Annotated, Any


# dependencies
from ..core.specs import Specs, TSpec
from ..core.typing import StrPath, TagBase


# constants
class Tag(TagBase):
    ID = auto()
    OF = auto()
    SKIPIF = auto()


@dataclass(frozen=True)
class Replace:
    """Annotation for replacer specs.

    Args:
        id: ID of data spec(s) to be replaced.
        of: Name of data spec attribute to be replaced.
        skipif: Sentinel value for which replacing is skipped.

    """

    id: Annotated[StrPath, Tag.ID]
    """ID of data spec(s) to be replaced."""

    of: Annotated[str, Tag.OF] = "data"
    """Name of data spec attribute to be replaced."""

    skipif: Annotated[Any, Tag.SKIPIF] = None
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
                    id=ID('/'),
                    tags=(),
                    type=<class '__main__.Weather'>,
                    data=Weather(temp=[20.0, 25.0], humid=[50.0, 55.0], dtype=<class 'int'>),
                ),
                Spec(
                    id=ID('/temp'),
                    tags=(<Tag.DATA: 2>,),
                    type=list[float],
                    data=[20.0, 25.0],
                ),
                Spec(
                    id=ID('/temp/0'),
                    tags=(<Tag.DTYPE: 3>,),
                    type=<class 'int'>, # <- replaced
                    data=None,
                ),
                Spec(
                    id=ID('/humid'),
                    tags=(<Tag.DATA: 2>,),
                    type=list[float],
                    data=[50.0, 55.0],
                ),
                Spec(
                    id=ID('/humid/0'),
                    tags=(<Tag.DTYPE: 3>,),
                    type=<class 'int'>, # <- replaced
                    data=None,
                ),
                Spec(
                    id=ID('/dtype'),
                    tags=(),
                    type=<class 'type'>,
                    data=<class 'int'>,
                ),
                Spec(
                    id=ID('/dtype/replace'),
                    tags=(),
                    type=<class 'dataspecs.extras.replacing.Replace'>,
                    data=Replace(id='/[a-z]+/0', of='type', skipif=None),
                ),
                Spec(
                    id=ID('/dtype/replace/id'),
                    tags=(<Tag.ID: 1>,),
                    type=<class 'str'>,
                    data='/(temp|humid)/0',
                ),
                Spec(
                    id=ID('/dtype/replace/of'),
                    tags=(<Tag.OF: 2>,),
                    type=<class 'str'>,
                    data='type',
                ),
                Spec(
                    id=ID('/dtype/replace/skipif'),
                    tags=(<Tag.SKIPIF: 3>,),
                    type=typing.Any,
                    data=None,
                ),
            ])

    """
    new = specs.copy()

    for spec in specs[Replace]:
        options = specs[spec.id.children]

        if (
            (id := options[Tag.ID].unique) is None
            or (of := options[Tag.OF].unique) is None
            or (skipif := options[Tag.SKIPIF].unique) is None
        ):
            continue

        if (replacer := specs[spec.id.parent].unique) is None:
            continue

        if replacer.data == skipif.data:
            continue

        for target in new[id[str].data]:
            changes = {of[str].data: replacer.data}
            updated = replace_(target, **changes)  # type: ignore
            new = new.replace(target, updated)

    return new
