# dependencies
from dataspecs import Attr, ID, Name, Spec, Tag, Type, Unit, Data
from dataspecs.core.spec import (
    is_attr,
    is_data,
    is_id,
    is_name,
    is_tag,
    is_type,
    is_unit,
)


# constants
SPEC = Spec(0, "/", "name", frozenset({"tag"}), int, None)


# test functions
def test_is_data() -> None:
    assert not is_data(Attr(0))
    assert is_data(Data(0))
    assert is_data(SPEC.data_)


def test_is_attr() -> None:
    assert not is_attr(0)
    assert is_attr(Attr(0))


def test_is_id() -> None:
    assert not is_id(Attr("/"))
    assert is_id(ID("/"))
    assert is_id(SPEC.id_)


def test_is_name() -> None:
    assert not is_name(Attr("name"))
    assert is_name(Name("name"))
    assert is_name(SPEC.name_)


def test_is_tag() -> None:
    assert not is_tag(Attr("tag"))
    assert is_tag(Tag("tag"))
    assert all(map(is_tag, SPEC.tags_))


def test_is_type() -> None:
    assert not is_type(Attr(int))
    assert is_type(Type(int))
    assert is_type(SPEC.type_)


def test_is_unit() -> None:
    assert not is_unit(Attr(None))
    assert is_unit(Unit(None))
    assert is_unit(SPEC.unit_)
