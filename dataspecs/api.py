__all__ = ["from_dataclass", "from_typehint"]


# standard library
from dataclasses import fields
from typing import Any


# dependencies
from .specs import Spec, Specs
from .typing import (
    ID,
    ROOT,
    DataClass,
    StrPath,
    get_annotated,
    get_dataclasses,
    get_subscriptions,
    get_tags,
)


def from_dataclass(
    obj: DataClass,
    /,
    *,
    parent: StrPath = ROOT,
    tagged_only: bool = True,
) -> Specs:
    """Create data specs from a dataclass object.

    Args:
        obj: Dataclass object to be parsed.
        parent: Path of the parent data spec.
        tagged_only: Whether to add only tagged data specs.

    Returns:
        Data specs created from the dataclass object.

    """
    specs = Specs()

    for f in fields(obj):
        if not (tags := get_tags(f.type)) and tagged_only:
            continue

        specs.append(
            Spec(
                id=(id := ID(parent) / f.name),
                type=(hint := get_annotated(f.type)),
                data=getattr(obj, f.name, f.default),
                tags=tags,
                origin=obj,
            )
        )
        specs.extend(
            from_typehint(
                hint,
                parent=id,
                tagged_only=tagged_only,
            )
        )

        for dc in get_dataclasses(f.type):
            specs.extend(
                from_dataclass(
                    dc,
                    parent=id,
                    tagged_only=tagged_only,
                )
            )

    return specs


def from_typehint(
    obj: Any,
    /,
    *,
    parent: StrPath = ROOT,
    tagged_only: bool = True,
) -> Specs:
    """Create data specs from a type hint.

    Args:
        obj: Type hint to be parsed.
        parent: Path of the parent data spec.
        tagged_only: Whether to add only tagged data specs.

    Returns:
        Data specs created from the type hint.

    """
    specs = Specs()

    for name, type in enumerate(get_subscriptions(obj)):
        if not (tags := get_tags(type)) and tagged_only:
            continue

        specs.append(
            Spec(
                id=(id := ID(parent) / str(name)),
                type=Any,
                data=(hint := get_annotated(type)),
                tags=tags,
                origin=obj,
            )
        )
        specs.extend(
            from_typehint(
                hint,
                parent=id,
                tagged_only=tagged_only,
            )
        )

        for dc in get_dataclasses(type):
            specs.extend(
                from_dataclass(
                    dc,
                    parent=id,
                    tagged_only=tagged_only,
                )
            )

    return specs
