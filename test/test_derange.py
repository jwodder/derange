import pytest
from   derange import derange

@pytest.mark.parametrize('iterable,output', [
    ([], []),
    ([42], [range(42, 43)]),
    ([2016, 2015, 2016], [range(2015, 2017)]),
    ([1, 5, 2, 4, 3], [range(1,6)]),
    ([1, 1, 5, 5, 2, 2, 4, 4, 3, 3], [range(1,6)]),
    ([1, 5, 3], [range(1,2), range(3,4), range(5,6)]),
    ([1, 5, 3, 4], [range(1,2), range(3,6)]),
    (
        [3,4,5,6,7,10,11,12,15,16,17,19,20,21,22,23,24,42,43,44,45,46],
        [range(3,8), range(10,13), range(15,18), range(19,25), range(42,47)],
    ),
    (
        [46,45,44,43,42,24,23,22,21,20,19,17,16,15,12,11,10,7,6,5,4,3],
        [range(3,8), range(10,13), range(15,18), range(19,25), range(42,47)],
    ),
    ([-1, -5, -2, -4, -3], [range(-5,0)]),
    ([-1, -1, -5, -5, -2, -2, -4, -4, -3, -3], [range(-5,0)]),
    ([-1, -5, -3], [range(-5,-4), range(-3,-2), range(-1,0)]),
    ([-1, -5, -3, -4], [range(-5,-2), range(-1,0)]),
])
def test_derange(iterable, output):
    assert derange(iterable) == output
