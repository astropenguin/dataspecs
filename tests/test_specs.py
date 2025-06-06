# standard library
from pathlib import PurePosixPath as Path


# dependencies
from dataspecs import Data, ID, Name, Spec, Specs, Tag, Type


# constants
SPECS = Specs(
    [
        Spec(
            data=[20.0, 25.0],
            id=Path("/temp"),
            name="Temperature",
            tags=frozenset({"data"}),
            type=list[float],
        ),
        Spec(
            data=None,
            id=Path("/temp/dtype"),
            name="dtype",
            tags=frozenset({"dtype"}),
            type=float,
        ),
        Spec(
            data="deg C",
            id=Path("/temp/units"),
            name="units",
            tags=frozenset({"attr"}),
            type=str,
        ),
        Spec(
            data="Air temperature measured at 1.5 m above the ground.",
            id=Path("/temp/long_name"),
            name="long_name",
            tags=frozenset({"attr"}),
            type=str,
        ),
        Spec(
            data=[3.0, 6.0],
            id=Path("/wind"),
            name="Wind speed",
            tags=frozenset({"data"}),
            type=list[float],
        ),
        Spec(
            data=None,
            id=Path("/wind/dtype"),
            name="dtype",
            tags=frozenset({"dtype"}),
            type=float,
        ),
        Spec(
            data="m/s",
            id=Path("/wind/units"),
            name="units",
            tags=frozenset({"attr"}),
            type=str,
        ),
        Spec(
            data="Wind speed measured at 1.5 m above the ground.",
            id=Path("/wind/long_name"),
            name="long_name",
            tags=frozenset({"attr"}),
            type=str,
        ),
        Spec(
            data="Tokyo",
            id=Path("/site"),
            name="Observation site",
            tags=frozenset({"attr"}),
            type=str,
        ),
        Spec(
            data=Data("K"),
            id=Path("/temp/units"),
            name="units",
            tags=frozenset(),
            type=Data,
        ),
        Spec(
            data=Data("km/h"),
            id=Path("/wind/units"),
            name="units",
            tags=frozenset(),
            type=Data,
        ),
    ]
)


# test functions
def test_Data_istype() -> None:
    assert Data.istype(Data(SPECS[0].data))
    assert not Data.istype(ID(SPECS[0].id))
    assert not Data.istype(Name(SPECS[0].name))
    assert not all(Data.istype(Tag(tag)) for tag in SPECS[0].tags)
    assert not Data.istype(Type(SPECS[0].type))


def test_Data_shift(new: int = 1, /) -> None:
    assert (Data(new) >> SPECS[0]).data == new
    assert (Data(new) >> SPECS[0]).data != SPECS[0].data


def test_Data_at(new: int = 1, /) -> None:
    assert Data(SPECS[0].data) @ SPECS[0]
    assert not Data(SPECS[0].data) @ SPECS[1]


def test_ID_istype() -> None:
    assert not ID.istype(Data(SPECS[0].data))
    assert ID.istype(ID(SPECS[0].id))
    assert not ID.istype(Name(SPECS[0].name))
    assert not all(ID.istype(Tag(tag)) for tag in SPECS[0].tags)
    assert not Data.istype(Type(SPECS[0].type))
    assert not ID.istype(Type(SPECS[0].type))


def test_ID_shift(new: Path = Path("/new"), /) -> None:
    assert (ID(new) >> SPECS[0]).id == new
    assert (ID(new) >> SPECS[0]).id != SPECS[0].id


def test_ID_at(new: Path = Path("/new"), /) -> None:
    assert ID(SPECS[0].id) @ SPECS[0]
    assert not ID(SPECS[0].id) @ SPECS[1]


def test_Name_istype() -> None:
    assert not Name.istype(Data(SPECS[0].data))
    assert not Name.istype(ID(SPECS[0].id))
    assert Name.istype(Name(SPECS[0].name))
    assert not all(Name.istype(Tag(tag)) for tag in SPECS[0].tags)
    assert not Name.istype(Type(SPECS[0].type))


def test_Name_shift(new: str = "new", /) -> None:
    assert (Name(new) >> SPECS[0]).name == new
    assert (Name(new) >> SPECS[0]).name != SPECS[0].name


def test_Name_at(new: str = "new", /) -> None:
    assert Name(SPECS[0].name) @ SPECS[0]
    assert not Name(SPECS[0].name) @ SPECS[1]


def test_Tag_istype() -> None:
    assert not Tag.istype(Data(SPECS[0].data))
    assert not Tag.istype(ID(SPECS[0].id))
    assert not Tag.istype(Name(SPECS[0].name))
    assert all(Tag.istype(Tag(tag)) for tag in SPECS[0].tags)
    assert not Tag.istype(Type(SPECS[0].type))


def test_Tag_shift(new: str = "new", /) -> None:
    assert (Tag(new) >> SPECS[0]).tags >= {new}
    assert (Tag(new) >> SPECS[0]).tags != SPECS[0].tags


def test_Tag_at(new: str = "new", /) -> None:
    assert all(Tag(tag) @ SPECS[0] for tag in SPECS[0].tags)
    assert not all(Tag(tag) @ SPECS[0] for tag in SPECS[1].tags)


def test_Type_istype() -> None:
    assert not Type.istype(Data(SPECS[0].data))
    assert not Type.istype(ID(SPECS[0].id))
    assert not Type.istype(Name(SPECS[0].name))
    assert not all(Type.istype(Tag(tag)) for tag in SPECS[0].tags)
    assert Type.istype(Type(SPECS[0].type))


def test_Type_shift(new: type = float, /) -> None:
    assert (Type(new) >> SPECS[0]).type == new
    assert (Type(new) >> SPECS[0]).type != SPECS[0].type


def test_Type_at(new: type = float, /) -> None:
    assert Type(SPECS[0].type) @ SPECS[0]
    assert not Type(SPECS[0].type) @ SPECS[1]


def test_specs_first() -> None:
    assert SPECS.first == SPECS[0]
    assert SPECS.first != SPECS[1]
    assert SPECS.first != SPECS[2]
    assert SPECS.first != SPECS[3]
    assert SPECS.first != SPECS[4]
    assert SPECS.first != SPECS[5]
    assert SPECS.first != SPECS[6]
    assert SPECS.first != SPECS[7]
    assert SPECS.first != SPECS[8]
    assert SPECS.first != SPECS[9]
    assert SPECS.first != SPECS[10]


def test_specs_last() -> None:
    assert SPECS.last != SPECS[0]
    assert SPECS.last != SPECS[1]
    assert SPECS.last != SPECS[2]
    assert SPECS.last != SPECS[3]
    assert SPECS.last != SPECS[4]
    assert SPECS.last != SPECS[5]
    assert SPECS.last != SPECS[6]
    assert SPECS.last != SPECS[7]
    assert SPECS.last != SPECS[8]
    assert SPECS.last != SPECS[9]
    assert SPECS.last == SPECS[10]


def test_specs_unique() -> None:
    assert SPECS[0:1].unique == SPECS[0]
    assert SPECS[1:2].unique == SPECS[1]
    assert SPECS[2:3].unique == SPECS[2]
    assert SPECS[3:4].unique == SPECS[3]
    assert SPECS[4:5].unique == SPECS[4]
    assert SPECS[5:6].unique == SPECS[5]
    assert SPECS[6:7].unique == SPECS[6]
    assert SPECS[7:8].unique == SPECS[7]
    assert SPECS[8:9].unique == SPECS[8]
    assert SPECS[9:10].unique == SPECS[9]
    assert SPECS[10:11].unique == SPECS[10]
    assert SPECS.unique is None


def test_specs_groupby() -> None:
    assert SPECS.groupby("id") == [
        SPECS[0:1],
        SPECS[1:2],
        SPECS[2:3] + SPECS[9:10],
        SPECS[3:4],
        SPECS[4:5],
        SPECS[5:6],
        SPECS[6:7] + SPECS[10:11],
        SPECS[7:8],
        SPECS[8:9],
    ]
    assert SPECS.groupby("name") == [
        SPECS[0:1],
        SPECS[1:2] + SPECS[5:6],
        SPECS[2:3] + SPECS[6:7] + SPECS[9:11],
        SPECS[3:4] + SPECS[7:8],
        SPECS[4:5],
        SPECS[8:9],
    ]
    assert SPECS.groupby("tags") == [
        SPECS[0:1] + SPECS[4:5],
        SPECS[1:2] + SPECS[5:6],
        SPECS[2:4] + SPECS[6:9],
        SPECS[9:11],
    ]
    assert SPECS.groupby("type") == [
        SPECS[0:1] + SPECS[4:5],
        SPECS[1:2] + SPECS[5:6],
        SPECS[2:4] + SPECS[6:9],
        SPECS[9:11],
    ]


def test_specs_merge() -> None:
    assert SPECS[9].data @ SPECS.merge()[2]
    assert SPECS[10].data @ SPECS.merge()[6]


def test_specs_getitem() -> None:
    assert SPECS[Data(list, type=True)] == SPECS[0:1] + SPECS[4:5]
    assert SPECS[ID("/temp.*", regex=True)] == SPECS[0:4] + SPECS[9:10]
    assert SPECS[ID("/wind.*", regex=True)] == SPECS[4:8] + SPECS[10:11]
    assert SPECS[Name("units")] == SPECS[2:3] + SPECS[6:7] + SPECS[9:11]
    assert SPECS[Tag("attr")] == SPECS[2:4] + SPECS[6:9]
    assert SPECS[Type(str)] == SPECS[2:4] + SPECS[6:9]


def test_specs_sub() -> None:
    assert SPECS - SPECS[Data(list, type=True)] == SPECS[1:4] + SPECS[5:11]
    assert SPECS - SPECS[ID("/temp.*", regex=True)] == SPECS[4:9] + SPECS[10:11]
    assert SPECS - SPECS[ID("/wind.*", regex=True)] == SPECS[0:4] + SPECS[8:10]
    assert SPECS - SPECS[Name("units")] == SPECS[0:2] + SPECS[3:6] + SPECS[7:9]
    assert SPECS - SPECS[Tag("attr")] == SPECS[0:2] + SPECS[4:6] + SPECS[9:11]
    assert SPECS - SPECS[Type(str)] == SPECS[0:2] + SPECS[4:6] + SPECS[9:11]
