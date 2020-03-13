.. image:: http://www.repostatus.org/badges/latest/active.svg
    :target: http://www.repostatus.org/#active
    :alt: Project Status: Active — The project has reached a stable, usable
          state and is being actively developed.

.. image:: https://travis-ci.org/jwodder/derange.svg?branch=master
    :target: https://travis-ci.org/jwodder/derange

.. image:: https://codecov.io/gh/jwodder/derange/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jwodder/derange

.. image:: https://img.shields.io/pypi/pyversions/derange.svg
    :target: https://pypi.org/project/derange

.. image:: https://img.shields.io/github/license/jwodder/derange.svg
    :target: https://opensource.org/licenses/MIT
    :alt: MIT License

.. image:: https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg
    :target: https://saythanks.io/to/jwodder

`GitHub <https://github.com/jwodder/derange>`_
| `PyPI <https://pypi.org/project/derange>`_
| `Issues <https://github.com/jwodder/derange/issues>`_

Do you have a list of integers?  Do you want to know what ranges of consecutive
values the list covers?  Do you need to solve a `gaps and islands
<https://stackoverflow.com/tags/gaps-and-islands/info>`_ problem outside of
SQL?  Maybe you have a list of dates and need to find the longest streak of
consecutive days on which something happened.  No?  Why not?  Well, either way,
the ``derange`` module is here for you, ready to solve all these problems and a
couple more.

Full documentation can be viewed after installation with ``python3 -m pydoc
derange``.


Installation
============
``derange`` requires Python 3.5 or higher.  Just use `pip
<https://pip.pypa.io>`_ for Python 3 (You have pip, right?) to install::

    python3 -m pip install derange


Examples
========
Condense commit years obtained from ``git log`` or the like into ``range``
objects::

    >>> import derange
    >>> derange.derange([2015, 2015, 2015, 2014, 2014, 2011, 2010, 2010, 2009, 2009])
    [range(2009, 2012), range(2014, 2016)]

If the input is already sorted, you can condense it slightly faster with
``derange_sorted``::

    >>> derange.derange_sorted([2009, 2009, 2010, 2010, 2011, 2014, 2014, 2015, 2015, 2015])
    [range(2009, 2012), range(2014, 2016)]

Organize non-integer values into closed intervals (represented as pairs of
endpoints) with ``deinterval``::

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

... which also has a ``deinterval_sorted`` variant::

    >>> derange.deinterval_sorted(within_24_hours, timestamps)
    [(datetime.datetime(2017, 11, 2, 12, 0), datetime.datetime(2017, 11, 6, 9, 0)), (datetime.datetime(2017, 11, 7, 10, 0), datetime.datetime(2017, 11, 7, 10, 0))]
    >>> derange.deinterval_sorted(within_24_hours, reversed(timestamps))
    Traceback (most recent call last):
        ...
    ValueError: sequence not in ascending order
