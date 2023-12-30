# standard library
from enum import auto


# dependencies
from dataspecs.core import Category


# test data
class Test(Category):
    MEMBER_1 = auto()
    MEMBER_2 = auto()


def test_category() -> None:
    assert Test.MEMBER_1 == "member_1"
    assert Test.MEMBER_2 == "member_2"
    assert Test("member_1") is Test.MEMBER_1
    assert Test("member_2") is Test.MEMBER_2
