import pytest

from ..types import int_in_range, float_in_range, path


@pytest.mark.parametrize('func, x, valid', [
    (int_in_range(0), '2', True),
    (int_in_range(0), '0', True),
    (int_in_range(2, 5), '6', False),
    (int_in_range(), 'a', False),
    (int_in_range(), '2.', False),
])
def test_int_in_range(func, x, valid):
    if valid:
        assert func(x) == int(x)
    else:
        with pytest.raises(ValueError):
            func(x)


@pytest.mark.parametrize('func, x, valid', [
    (float_in_range(0), '2', True),
    (float_in_range(0), '0', True),
    (float_in_range(0, inclusive=False), '0', False),
    (float_in_range(), 'a', False),
    (float_in_range(), 'inf', False),
])
def test_float_in_range(func, x, valid):
    if valid:
        assert func(x) == float(x)
    else:
        with pytest.raises(ValueError):
            func(x)


def test_path():
    assert path("A//B") == path("A/B/") == path("A/./B") == path("A/foo/../B") == "A/B"


@pytest.mark.parametrize('func, expected_name', [
    (int_in_range(0), 'nonnegative_int'),
    (int_in_range(1), 'positive_int'),
    (int_in_range(2), 'int∈[2, ∞)'),
    (int_in_range(2, 5), 'int∈[2, 5]'),
    (float_in_range(0.), 'nonnegative_float'),
    (float_in_range(0., inclusive=False), 'positive_float'),
    (float_in_range(1.), 'float∈[1.0, ∞)'),
    (float_in_range(1., inclusive=False), 'float∈(1.0, ∞)'),
])
def test_name(func, expected_name):
    assert func.__name__ == expected_name
