import pytest
from   derange import deinterval

def delta1(a,b):
    return abs(a-b) <= 1

@pytest.mark.parametrize('predicate,iterable,output', [
    (delta1, [], []),
    (delta1, [42], [(42, 42)]),
    (delta1, [2016, 2015, 2016], [(2015, 2016)]),
    (delta1, [1, 5, 2, 4, 3], [(1,5)]),
    (delta1, [1, 1, 5, 5, 2, 2, 4, 4, 3, 3], [(1,5)]),
    (delta1, [1, 5, 3], [(1,1), (3,3), (5,5)]),
    (delta1, [1, 5, 3, 4], [(1,1), (3,5)]),
    (
        delta1,
        [3,4,5,6,7,10,11,12,15,16,17,19,20,21,22,23,24,42,43,44,45,46],
        [(3,7), (10,12), (15,17), (19,24), (42,46)],
    ),
    (
        delta1,
        [46,45,44,43,42,24,23,22,21,20,19,17,16,15,12,11,10,7,6,5,4,3],
        [(3,7), (10,12), (15,17), (19,24), (42,46)],
    ),
    (delta1, [1, 1.5, 2.4], [(1, 2.4)]),
    (delta1, [1, 1.5, 2.6], [(1, 1.5), (2.6, 2.6)]),
    (delta1, [1, 1.5, 1.4], [(1, 1.5)]),
    (delta1, [1, 1.5, 2.6, 2], [(1, 2.6)]),
    (
        lambda a,b: a[:3] == b[:3], '''
            potato potato potentate potate
            tomato tomahawk toml tunnel tonight
            snake snack snipe snark swipe
            potion pot potent portable potable
        '''.split(),
        [
            ('portable', 'portable'),
            ('pot', 'potion'),
            ('snack', 'snark'),
            ('snipe', 'snipe'),
            ('swipe', 'swipe'),
            ('tomahawk', 'toml'),
            ('tonight', 'tonight'),
            ('tunnel', 'tunnel'),
        ],
    ),
    (delta1, [-1, -5, -2, -4, -3], [(-5,-1)]),
    (delta1, [-1, -1, -5, -5, -2, -2, -4, -4, -3, -3], [(-5,-1)]),
    (delta1, [-1, -5, -3], [(-5,-5), (-3,-3), (-1,-1)]),
    (delta1, [-1, -5, -3, -4], [(-5,-3), (-1,-1)]),
    (delta1, [-1, -1.5, -2.4], [(-2.4, -1)]),
    (delta1, [-1, -1.5, -2.6], [(-2.6, -2.6), (-1.5, -1)]),
    (delta1, [-1, -1.5, -1.4], [(-1.5, -1)]),
    (delta1, [-1, -1.5, -2.6, -2], [(-2.6, -1)]),
])
def test_deinterval(predicate, iterable, output):
    assert deinterval(predicate, iterable) == output
