__all__ = ["Replace", "ReplaceTag", "replace"]


# standard library
from dataclasses import dataclass, replace as replace_
from enum import auto
from typing import Annotated, Any


# dependencies
from ..core.specs import SpecAttr, SpecIndex, Specs, TSpec
from ..core.typing import TagBase


# constants
class ReplaceTag(TagBase):
    """Collection of tags for replacer specs."""

    ATTR = auto()
    """Tag for name of data spec attribute to be replaced."""

    INDEX = auto()
    """Tag for index of data spec(s) to be replaced."""

    SKIPIF = auto()
    """Tag for sentinel value for which replacing is skipped."""


@dataclass(frozen=True)
class Replace:
    """Annotation for replacer specs.

    Args:
        _replace_index: Index of data spec(s) to be replaced.
        _replace_attr: Name of data spec attribute to be replaced.
        _replace_skipif: Sentinel value for which replacing is skipped.

    """

    _replace_index: Annotated[SpecIndex, ReplaceTag.INDEX]
    """Index of data spec(s) to be replaced."""

    _replace_attr: Annotated[SpecAttr, ReplaceTag.ATTR] = "data"
    """Name of data spec attribute to be replaced."""

    _replace_skipif: Annotated[Any, ReplaceTag.SKIPIF] = None
    """Sentinel value for which replacing is skipped."""


def replace(specs: Specs[TSpec], /, *, leave: bool = False) -> Specs[TSpec]:
    """Replace data spec attributes by replacer specs.

    Args:
        specs: Input data specs.
        leave: Whether to leave the replacer specs.

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
                    name='temp',
                    tags=(<Tag.DATA: 2>,),
                    type=list[float],
                    data=[20.0, 25.0],
                ),
                Spec(
                    path=Path('/temp/0'),
                    name='0',
                    tags=(<Tag.DTYPE: 3>,),
                    type=<class 'int'>, # <- replaced
                    data=None,
                ),
                Spec(
                    path=Path('/humid'),
                    name='humid',
                    tags=(<Tag.DATA: 2>,),
                    type=list[float],
                    data=[50.0, 55.0],
                ),
                Spec(
                    path=Path('/humid/0'),
                    name='0',
                    tags=(<Tag.DTYPE: 3>,),
                    type=<class 'int'>, # <- replaced
                    data=None,
                ),
                Spec(
                    path=Path('/dtype'),
                    name='dtype',
                    tags=(),
                    type=<class 'type'>,
                    data=<class 'int'>,
                ),
            ])

    """
    new = specs.copy()

    for spec in specs:
        for options in specs[spec.path.children].groupby("orig", method="id"):
            if (
                (index := options[ReplaceTag.INDEX].unique) is None
                or (attr := options[ReplaceTag.ATTR].unique) is None
                or (skipif := options[ReplaceTag.SKIPIF].unique) is None
            ):
                continue

            if spec.data == skipif.data:
                continue

            for target in new(index.data):
                changes = {attr[str].data: spec.data}
                new = new.replace(target, replace_(target, **changes))

            if not leave:
                new.remove(index)
                new.remove(attr)
                new.remove(skipif)

    return new
