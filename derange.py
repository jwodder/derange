"""
Compress lists of integers to range objects

Do you have a list of integers?  Do you want to know what ranges of consecutive
values the list covers?  Do you need to solve a `gaps and islands
<https://stackoverflow.com/tags/gaps-and-islands/info>`_ problem outside of
SQL?  Maybe you have a list of dates and need to find the longest streak of
consecutive days on which something happened.  No?  Why not?  Well, either way,
the `derange` module is here for you, ready to solve all these problems and a
couple more.

Visit <https://github.com/jwodder/derange> for more information.
"""

__version__      = '0.1.0'
__author__       = 'John Thorvald Wodder II'
__author_email__ = 'derange@varonathe.org'
__license__      = 'MIT'
__url__          = 'https://github.com/jwodder/derange'

def derange(iterable):
    """
    Convert a sequence of integers to a minimal list of `range` objects that
    together contain all of the input elements.

    Output is in strictly ascending order.  Input need not be in order (but see
    also `derange_sorted()`).  Duplicate input values are ignored.

    >>> derange([3,4,5,6,7,10,11,12,15,16,17,19,20,21,22,23,24,42,43,44,45,46])
    [range(3, 8), range(10, 13), range(15, 18), range(19, 25), range(42, 47)]

    >>> derange([2016, 2015, 2016])
    [range(2015, 2017)]

    >>> derange([42])
    [range(42, 43)]

    >>> derange([])
    []
    """
    ranges = []
    for x in iterable:
        if not ranges:
            ranges = [range(x, x+1)]
        elif x < ranges[0].start - 1:
            ranges.insert(0, range(x, x+1))
        elif x > ranges[-1].stop:
            ranges.append(range(x, x+1))
        else:
            low, high = 0, len(ranges)
            while low < high:
                mid = (low + high) // 2
                if x in ranges[mid]:
                    break
                elif x == ranges[mid].start - 1:
                    if mid > 0 and ranges[mid-1].stop == x:
                        ranges[mid-1:mid+1] \
                            = [range(ranges[mid-1].start, ranges[mid].stop)]
                    else:
                        ranges[mid] = range(x, ranges[mid].stop)
                    break
                elif x == ranges[mid].stop:
                    if mid+1 < len(ranges) and ranges[mid+1].start == x+1:
                        ranges[mid:mid+2] \
                            = [range(ranges[mid].start, ranges[mid+1].stop)]
                    else:
                        ranges[mid] = range(ranges[mid].start, x+1)
                    break
                elif x < ranges[mid].start:
                    high = mid
                else:
                    assert x > ranges[mid].stop
                    low = mid + 1
            else:
                ranges.insert(low, range(x, x+1))
    return ranges

def deinterval(adjacent, iterable):
    """
    Convert a sequence of totally-ordered values to a minimal list of closed
    intervals (represented as pairs of endpoints) that together contain all of
    the input elements.  This is a generalization of `derange()` for arbitrary
    types.

    Two input values will be placed in the same interval iff they are directly
    adjacent or there exists a chain of adjacent input values connecting them,
    where adjacency is defined by the given ``adjacent`` callable.

    Output is in strictly ascending order.  Input need not be in order (but see
    also `deinterval_sorted()`).  Duplicate input values are ignored.

    Note that, unlike with `range` objects, intervals returned from
    `deinterval()` contain their upper bounds.

    >>> def within_three(x, y):
    ...     return abs(x-y) <= 3
    ... 
    >>> deinterval(within_three, [1.1, 2.2, 3.3, 5.5, 7.7, 8.8])
    [(1.1, 8.8)]
    >>> deinterval(within_three, [1.1, 2.2, 3.3, 6.6, 7.7, 8.8])
    [(1.1, 3.3), (6.6, 8.8)]

    :param callable adjacent: Called with two elements of ``iterable`` at a
        time to test whether they should be placed in the same interval.
        The binary relation implied by ``adjacent`` must be reflexive and
        symmetric, and for all ``x < y < z``, if ``adjacent(x, z)`` is true,
        then both ``adjacent(x, y)`` and ``adjacent(y, z)`` must also be true.
    :param iterable iterable: a sequence of values that can be sorted/totally
        ordered
    :return: a list of pairs of elements of ``iterable`` in strictly ascending
        order
    """
    intervals = []
    for x in iterable:
        if not intervals:
            intervals = [(x,x)]
        elif x < intervals[0][0]  and not adjacent(x, intervals[0][0]):
            intervals.insert(0, (x,x))
        elif x > intervals[-1][1] and not adjacent(x, intervals[-1][1]):
            intervals.append((x,x))
        else:
            low, high = 0, len(intervals)
            while low < high:
                mid = (low + high) // 2
                a, b = intervals[mid]
                if a <= x <= b:
                    break
                elif x < a:
                    if not adjacent(x, a):
                        high = mid
                    elif mid > 0 and adjacent(intervals[mid-1][1], x):
                        intervals[mid-1:mid+1] = [(intervals[mid-1][0], b)]
                        break
                    else:
                        intervals[mid] = (x, b)
                        break
                else:
                    assert x > b
                    if not adjacent(x, b):
                        low = mid + 1
                    elif mid+1 < len(intervals) and \
                            adjacent(intervals[mid+1][0], x):
                        intervals[mid:mid+2] = [(a, intervals[mid+1][1])]
                        break
                    else:
                        intervals[mid] = (a, x)
                        break
            else:
                intervals.insert(low, (x,x))
    return intervals

def derange_sorted(iterable):
    """
    Convert a *non-decreasing* sequence of integers to a minimal list of
    `range` objects that together contain all of the input elements.  This is
    faster than `derange()` but only accepts sorted input.

    :raises ValueError: if ``iterable`` is not sorted
    """
    ranges = []
    for x in iterable:
        try:
            end = ranges[-1]
        except IndexError:
            ranges = [range(x, x+1)]
        else:
            if x == end.stop - 1:
                pass
            elif x == end.stop:
                ranges[-1] = range(end.start, x+1)
            elif x > end.stop:
                ranges.append(range(x, x+1))
            else:
                raise ValueError('sequence not in ascending order')
    return ranges

def deinterval_sorted(adjacent, iterable):
    """
    Convert a *non-decreasing* sequence of totally-ordered values to a minimal
    list of closed intervals that together contain all of the input elements.
    This is faster than `deinterval()` but only accepts sorted input.

    :raises ValueError: if ``iterable`` is not sorted
    """
    intervals = []
    for x in iterable:
        try:
            a,b = intervals[-1]
        except IndexError:
            intervals = [(x,x)]
        else:
            if x == b:
                pass
            elif x > b:
                if adjacent(x, b):
                    intervals[-1] = (a, x)
                else:
                    intervals.append((x,x))
            else:
                raise ValueError('sequence not in ascending order')
    return intervals
