import itertools


def assert_equal(target, answer):
    assert _check_equal_all(target, answer)


def _check_equal_all(target, answer):
    if type(target) != type(answer):
        return False
    if isinstance(target, tuple) or isinstance(target, list):
        return all([_check_equal_all(a, b) for a, b in itertools.zip_longest(target, answer)])
    elif isinstance(target, dict):
        return all(
            [_check_equal_all(a, b) for a, b in itertools.zip_longest(
                sorted(target.items()), sorted(answer.items()))])
    else:
        return target == answer


def assertIsNone(a):
    assert a is None
