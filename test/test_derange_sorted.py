import pytest
from   derange import derange_sorted

@pytest.mark.parametrize('iterable,output', [
    ([], []),
    ([42], [range(42, 43)]),
    ([1,2], [range(1,3)]),
    ([1,2,2], [range(1,3)]),
    ([1,2,3], [range(1,4)]),
    ([1,2,4], [range(1,3), range(4,5)]),
    ([1,2,2,4], [range(1,3), range(4,5)]),
    ([1,2,2,4,4], [range(1,3), range(4,5)]),
    ([1,2,17], [range(1,3), range(17,18)]),
    (
        [3,4,5,6,7,10,11,12,15,16,17,19,20,21,22,23,24,42,43,44,45,46],
        [range(3,8), range(10,13), range(15,18), range(19,25), range(42,47)],
    ),
    (
        [-46,-45,-44,-43,-42,-24,-23,-22,-21,-20,-19,-17,-16,-15,-12,-11,-10,-7,-6,-5,-4,-3],
        [range(-46, -41), range(-24, -18), range(-17, -14), range(-12, -9), range(-7, -2)],
    ),
])
def test_derange_sorted(iterable, output):
    assert derange_sorted(iterable) == output

@pytest.mark.parametrize('iterable', [
    [46,45,44,43,42,24,23,22,21,20,19,17,16,15,12,11,10,7,6,5,4,3],
    [-3,-4,-5,-6,-7,-10,-11,-12,-15,-16,-17,-19,-20,-21,-22,-23,-24,-42,-43,-44,-45,-46],
    [1,2,4,3],
    [-1,-2,-2,-4],
])
def test_bad_derange_sorted(iterable):
    with pytest.raises(ValueError, message='sequence not in ascending order'):
        derange_sorted(iterable)
