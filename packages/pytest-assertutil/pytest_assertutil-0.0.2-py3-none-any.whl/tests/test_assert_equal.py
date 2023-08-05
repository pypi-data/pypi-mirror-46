from pytest_assertutil import assert_equal
from fractions import Fraction
import pytest


def test_assert_equal_int():
    assert_equal(1, 1)


def test_assert_equal_float():
    assert_equal(1.0, 1.0)


def test_assert_equal_tuple():
    assert_equal((1, 2), (1, 2))


def test_assert_equal_tuple_reversed():
    assert_equal((1, 2), (2, 1))


def test_assert_equal_list():
    assert_equal([1, 2], [1, 2])


def test_assert_equal_list_reverse_order():
    assert_equal([1, 2], [2, 1])


def test_assert_equal_dict():
    assert_equal({1: 2, 3: 4}, {1: 2, 3: 4})


def test_assert_equal_dict_reverse_order():
    assert_equal({1: 2, 3: 4}, {3: 4, 1: 2})


def test_assert_equal_complex():
    assert_equal(
        {
            1: (2, [3, 4, {5: 6, 7: 8}], 9, 10),
            11: (12, [13, 14, {15: 16, 17: 18}], 19, 20)
        },
        {
            1: (2, [3, 4, {5: 6, 7: 8}], 9, 10),
            11: (12, [13, 14, {15: 16, 17: 18}], 19, 20)
        }
    )


def test_assert_equal_complex_shuffled():
    assert_equal(
        {
            1: (2, [3, 4, {5: 6, 7: 8}], 9, 10),
            11: (12, [13, 14, {15: 16, 17: 18}], 19, 20)
        },
        {
            11: (20, [{17: 18, 15: 16}, 13, 14], 19, 12),
            1: (2, [3, 4, {5: 6, 7: 8}], 9, 10)
        }
    )


def test_fraction_class():
    assert_equal(Fraction(2, 5), Fraction(2, 5))


def test_assert_equal_complex_shuffled_with_fraction():
    assert_equal(
        {
            1: (2, [3, 4, {5: 6, 7: 8}], 9, 10, Fraction(2, 5)),
            11: (12, [13, 14, {15: 16, 17: 18}], 19, 20)
        },
        {
            11: (20, [{17: 18, 15: 16}, 13, 14], 19, 12),
            1: (2, [3, 4, {5: 6, 7: 8}], 9, 10, Fraction(2, 5))
        }
    )


@pytest.mark.xfail(raises=AssertionError)
def test_assert_equal_intE():
    assert_equal(1, 2)


@pytest.mark.xfail(raises=AssertionError)
def test_assert_equal_floatE():
    assert_equal(1.0, 2.0)


@pytest.mark.xfail(raises=AssertionError)
def test_assert_equal_tupleE1():
    assert_equal((1, 2), (1, 2, 3))


@pytest.mark.xfail(raises=AssertionError)
def test_assert_equal_tupleE2():
    assert_equal((1, 2), (1, 3))


@pytest.mark.xfail(raises=AssertionError)
def test_assert_equal_listE1():
    assert_equal([1, 2], [1, 2, 3])


@pytest.mark.xfail(raises=AssertionError)
def test_assert_equal_listE2():
    assert_equal([1, 2], [1, 3])


@pytest.mark.xfail(raises=AssertionError)
def test_assert_equal_listE3():
    assert_equal([1, 2], (1, 2))


@pytest.mark.xfail(raises=AssertionError)
def test_assert_equal_dictE1():
    assert_equal({1: 2, 3: 4}, {1: 2, 3: 5})


@pytest.mark.xfail(raises=AssertionError)
def test_assert_equal_dictE2():
    assert_equal({1: 2, 3: 4}, {1: 2, 3: 4, 5: 6})


@pytest.mark.xfail(raises=AssertionError)
def test_assert_equal_dictE3():
    assert_equal({1: 2, 3: 4}, [(1, 2), (3, 4)])
