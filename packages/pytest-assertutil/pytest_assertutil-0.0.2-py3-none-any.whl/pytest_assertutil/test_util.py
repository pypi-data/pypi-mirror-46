import itertools
from decimal import Decimal

_numeric_type = (int, float, Decimal)
_list_tuple = (list, tuple)


def multitype_key(v):
    vtype = type(v)
    if vtype in _numeric_type:
        return "a%050.8f" % v
    if isinstance(v, str):
        return "b%s" % v
    if vtype in _list_tuple:
        return "c%s" % str(v)
    if isinstance(v, dict):
        return "d%s" % str(v)
    return str(v)


def assert_equal(target, answer):
    assert _check_equal_all(target, answer)


def _check_equal_all(target, answer):
    target_type = type(target)
    answer_type = type(answer)
    if isinstance(target, tuple) or isinstance(target, list):
        if target_type != answer_type:
            return False
        return all(
            [_check_equal_all(a, b)
             for a, b in itertools.zip_longest(
                sorted(target, key=multitype_key),
                sorted(answer, key=multitype_key))])
    elif isinstance(target, dict):
        if target_type != answer_type:
            return False
        return all(
            [_check_equal_all(a, b) for a, b in itertools.zip_longest(
                sorted(target.items(), key=multitype_key),
                sorted(answer.items(), key=multitype_key))])
    elif target_type != answer_type:
        return False
    else:
        return target == answer
