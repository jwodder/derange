.. image:: http://www.repostatus.org/badges/latest/active.svg
    :target: http://www.repostatus.org/#active
    :alt: Project Status: Active — The project has reached a stable, usable
          state and is being actively developed.

.. image:: https://github.com/jwodder/derange/workflows/Test/badge.svg?branch=master
    :target: https://github.com/jwodder/derange/actions?workflow=Test
    :alt: CI Status

.. image:: https://codecov.io/gh/jwodder/derange/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jwodder/derange

.. image:: https://img.shields.io/pypi/pyversions/derange.svg
    :target: https://pypi.org/project/derange

.. image:: https://img.shields.io/github/license/jwodder/derange.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

`GitHub <https://github.com/jwodder/derange>`_
| `PyPI <https://pypi.org/project/derange>`_
| `Issues <https://github.com/jwodder/derange/issues>`_
| `Changelog <https://github.com/jwodder/derange/blob/master/CHANGELOG.md>`_

Do you have a list of integers?  Do you want to know what ranges of consecutive
values the list covers?  Do you need to solve a `gaps and islands
<https://stackoverflow.com/tags/gaps-and-islands/info>`_ problem outside of
SQL?  Maybe you have a list of dates and need to find the longest streak of
consecutive days on which something happened.  No?  Why not?  Well, either way,
the ``derange`` module is here for you, ready to solve all these problems and a
couple more.


Installation
============
``derange`` requires Python 3.7 or higher.  Just use `pip
<https://pip.pypa.io>`_ for Python 3 (You have pip, right?) to install::

    python3 -m pip install derange


Examples
========
Condense commit years obtained from ``git log`` or the like into ``range``
objects:

>>> import derange
>>> derange.derange([2015, 2015, 2015, 2014, 2014, 2011, 2010, 2010, 2009, 2009])
[range(2009, 2012), range(2014, 2016)]

If the input is already sorted, you can condense it slightly faster with
``derange_sorted()``:

>>> derange.derange_sorted([2009, 2009, 2010, 2010, 2011, 2014, 2014, 2015, 2015, 2015])
[range(2009, 2012), range(2014, 2016)]

Organize non-integer values into closed intervals (represented as pairs of
endpoints) with ``deinterval()``:

>>> import datetime
>>> # deinterval() requires a callable for determining when two values are "adjacent":
>>> def within_24_hours(a,b):
...     return abs(a-b) <= datetime.timedelta(hours=24)
...
>>> timestamps = [
...     datetime.datetime(2017, 11, 2, 12, 0),
...     datetime.datetime(2017, 11, 3, 11, 0),
...     datetime.datetime(2017, 11, 4, 10, 0),
...     datetime.datetime(2017, 11, 5,  9, 0),
...     datetime.datetime(2017, 11, 6,  9, 0),
...     datetime.datetime(2017, 11, 7, 10, 0),
... ]
>>> derange.deinterval(within_24_hours, timestamps)
[(datetime.datetime(2017, 11, 2, 12, 0), datetime.datetime(2017, 11, 6, 9, 0)), (datetime.datetime(2017, 11, 7, 10, 0), datetime.datetime(2017, 11, 7, 10, 0))]

… which also has a ``deinterval_sorted()`` variant:

>>> derange.deinterval_sorted(within_24_hours, timestamps)
[(datetime.datetime(2017, 11, 2, 12, 0), datetime.datetime(2017, 11, 6, 9, 0)), (datetime.datetime(2017, 11, 7, 10, 0), datetime.datetime(2017, 11, 7, 10, 0))]
>>> derange.deinterval_sorted(within_24_hours, reversed(timestamps))
Traceback (most recent call last):
    ...
ValueError: sequence not in ascending order


API
===

.. code:: python

    derange.derange(iterable: Iterable[int]) -> List[range]

Convert a sequence of integers to a minimal list of ``range`` objects that
together contain all of the input elements.

Output is in strictly ascending order.  Input need not be in order (but see
also ``derange_sorted()``).  Duplicate input values are ignored.

.. code:: python

    derange.derange_sorted(iterable: Iterable[int]) -> List[range]

Convert a *non-decreasing* sequence of integers to a minimal list of ``range``
objects that together contain all of the input elements.  This is faster than
``derange()`` but only accepts sorted input.

.. code:: python

    derange.deinterval(
        adjacent: Callable[[T,T], bool],
        iterable: Iterable[T],
    ) -> List[Tuple[T,T]]

Convert a sequence of totally-ordered values to a minimal list of closed
intervals (represented as pairs of endpoints) that together contain all of the
input elements.  This is a generalization of ``derange()`` for arbitrary types.

Two input values will be placed in the same interval iff they are directly
adjacent or there exists a chain of adjacent input values connecting them,
where adjacency is defined by the given ``adjacent`` callable.

``adjacent`` will be called with two elements of ``iterable`` at a time to test
whether they should be placed in the same interval.  The binary relation
implied by ``adjacent`` must be reflexive and symmetric, and for all ``x < y <
z``, if ``adjacent(x, z)`` is true, then both ``adjacent(x, y)`` and
``adjacent(y, z)`` must also be true.

Output is in strictly ascending order.  Input need not be in order (but see
also ``deinterval_sorted()``).  Duplicate input values are ignored.

Note that, unlike with ``range`` objects, intervals returned from
``deinterval()`` contain their upper bounds.

.. code:: python

    derange.deinterval_sorted(
        adjacent: Callable[[T,T], bool],
        iterable: Iterable[T],
    ) -> List[Tuple[T,T]]

Convert a *non-decreasing* sequence of totally-ordered values to a minimal list
of closed intervals that together contain all of the input elements.  This is
faster than ``deinterval()`` but only accepts sorted input.
