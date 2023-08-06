import pytest
from watched import generate_nth_fibonacci


@pytest.mark.parametrize(
    ('n', 'expected'), [
        (0, 0),
        (1, 1),
        (2, 1),
        (3, 2),
        (4, 3),
        (5, 5),
        (20, 6765),
    ]
)
def test_nth_fibonacci(n, expected):
    actual = generate_nth_fibonacci(n)
    assert actual == expected


def test_negative_input_fibonacci():
    with pytest.raises(ValueError):
        generate_nth_fibonacci(-1)
