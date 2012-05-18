"""
GrandFatherSon is a backup rotation calculator that implements the
`grandfather-father-son rotation scheme
<http://en.wikipedia.org/wiki/Backup_rotation_scheme#Grandfather-father-son_backup>`_.

This is usually done by keeping a certain number of daily, weekly, and
monthly backups. Older backups should be removed to reduce the amount
of space used.


Usage
-----

This module expects either ``datetime.date`` or ``datetime.datetime``
objects as inputs. As an example, let's assume you have daily backups
for the all of year 1999 that need rotating::

    >>> import datetime
    >>> start_date = datetime.date(1999, 1, 1)
    >>> end_date = datetime.date(1999, 12, 31)
    >>> backups = [start_date + datetime.timedelta(days=i)
    ...            for i in xrange((end_date - start_date).days + 1)]
    >>> backups
    [datetime.date(1999, 1, 1),
     datetime.date(1999, 1, 2),
     datetime.date(1999, 1, 3),
     ...
     datetime.date(1999, 12, 30),
     datetime.date(1999, 12, 31)]

Let's say that full backups are taken every Saturday, with incremental
backups done daily. A week, or 7 days, of incremental backups should
be kept. A months, or 4 weeks, of full backups are kept. In addition,
for three months, the first full backup is kept for each month, with
the others discarded.

It's the last day of the year and you want to figure out which backups
need to be pruned::

    >>> now = datetime.date(1999, 12, 31)

To see which files will be preserved, use the ``dates_to_keep``
function::

    >>> from grandfatherson import dates_to_keep, SATURDAY
    >>> sorted(dates_to_keep(backups, days=7, weeks=4, months=3,
    ...                      firstweekday=SATURDAY, now=now))
    [datetime.date(1999, 10, 1),
     datetime.date(1999, 11, 1),
     datetime.date(1999, 12, 1),
     datetime.date(1999, 12, 4),
     datetime.date(1999, 12, 11),
     datetime.date(1999, 12, 18),
     datetime.date(1999, 12, 25),
     datetime.date(1999, 12, 26),
     datetime.date(1999, 12, 27),
     datetime.date(1999, 12, 28),
     datetime.date(1999, 12, 29),
     datetime.date(1999, 12, 30),
     datetime.date(1999, 12, 31)]

If you leave off the ``now`` argument, it will default to using
``datetime.datetime.now()``.

To see which files should be deleted, use the ``dates_to_delete``
function::

    >>> from grandfatherson import dates_to_keep, SATURDAY
    >>> sorted(dates_to_delete(backups, days=7, weeks=4, months=3,
    ...                        firstweekday=SATURDAY, now=now))
    [datetime.date(1999, 1, 1),
     ...
     datetime.date(1999, 9, 30),
     datetime.date(1999, 10, 2),
     ...
     datetime.date(1999, 10, 31),
     datetime.date(1999, 11, 2),
     ...
     datetime.date(1999, 11, 30),
     datetime.date(1999, 12, 2),
     datetime.date(1999, 12, 3),
     datetime.date(1999, 12, 5),
     ...
     datetime.date(1999, 12, 10),
     datetime.date(1999, 12, 12),
     ...
     datetime.date(1999, 12, 17),
     datetime.date(1999, 12, 19),
     ...
     datetime.date(1999, 12, 24)]

Finally, if you need to rotate backups that have timestamps in
``datetime`` format, you can use the corresponding ``to_keep`` and
``to_delete`` functions::

    >>> now = datetime.datetime(1999, 12, 31, 23, 59, 59)
    >>> start_datetime = datetime.datetime(1999, 12, 31, 0, 0, 0)
    >>> end_datetime = datetime.datetime(1999, 12, 31, 23, 59, 59)
    >>> backups = [start_datetime + datetime.timedelta(seconds=i)
    ...            for i
    ...            in xrange((end_datetime - start_datetime).seconds + 1)]
    >>> backups
    [datetime.datetime(1999, 12, 31, 0, 0),
     datetime.datetime(1999, 12, 31, 0, 0, 1),
     datetime.datetime(1999, 12, 31, 0, 0, 2),
     ...
     datetime.datetime(1999, 12, 31, 23, 59, 58),
     datetime.datetime(1999, 12, 31, 23, 59, 59)]

    >>> from grandfatherson import to_keep
    >>> sorted(to_keep(backups, hours=2, minutes=10, seconds=10, now=now))
    [datetime.datetime(1999, 12, 31, 22, 0),
     datetime.datetime(1999, 12, 31, 23, 0),
     datetime.datetime(1999, 12, 31, 23, 50),
     ...
     datetime.datetime(1999, 12, 31, 23, 59),
     datetime.datetime(1999, 12, 31, 23, 59, 50),
     ...
     datetime.datetime(1999, 12, 31, 23, 59, 59)]

    >>> from grandfatherson import to_delete
    >>> sorted(to_delete(backups, hours=2, minutes=10, seconds=10, now=now))
    [datetime.datetime(1999, 12, 31, 0, 0),
     ...
     datetime.datetime(1999, 12, 31, 21, 59, 59),
     datetime.datetime(1999, 12, 31, 22, 0, 1),
     ...
     datetime.datetime(1999, 12, 31, 22, 59, 59),
     datetime.datetime(1999, 12, 31, 23, 0, 1),
     ...
     datetime.datetime(1999, 12, 31, 23, 49, 59),
     datetime.datetime(1999, 12, 31, 23, 50, 1),
     ...
     datetime.datetime(1999, 12, 31, 23, 58, 59),
     datetime.datetime(1999, 12, 31, 23, 59, 1),
     ...
     datetime.datetime(1999, 12, 31, 23, 59, 49)]
"""

from calendar import (MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY,
                      SUNDAY)
from datetime import datetime, time
import os

from grandfatherson import filters


def to_keep(datetimes,
            years=0, months=0, weeks=0, days=0,
            hours=0, minutes=0, seconds=0,
            firstweekday=SATURDAY, now=None):
    """
    Return a set of datetimes that should be kept, out of ``datetimes``.

    Keeps up to ``years``, ``months``, ``weeks``, ``days``,
    ``hours``, ``minutes``, and ``seconds`` in the past.

    When keeping weeks, it prefers to keep ``firstweekday``, which
    defaults to Saturday.

    If ``now`` is None, it will base its calculations on
    ``datetime.datetime.now()``. Datetimes after this point will always be
    kept.
    """
    datetimes = set(datetimes)
    return (filters.Years.filter(datetimes, number=years, now=now) |
            filters.Months.filter(datetimes, number=months, now=now) |
            filters.Weeks.filter(datetimes, number=weeks,
                                 firstweekday=firstweekday, now=now) |
            filters.Days.filter(datetimes, number=days, now=now) |
            filters.Hours.filter(datetimes, number=hours, now=now) |
            filters.Minutes.filter(datetimes, number=minutes, now=now) |
            filters.Seconds.filter(datetimes, number=seconds, now=now))


def to_delete(datetimes,
              years=0, months=0, weeks=0, days=0,
              hours=0, minutes=0, seconds=0,
              firstweekday=SATURDAY, now=None):
    """
    Return a set of datetimes that should be deleted, out of ``datetimes``.

    See ``to_keep`` for a description of arguments.
    """
    datetimes = set(datetimes)
    return datetimes - to_keep(datetimes,
                               years=years, months=months,
                               weeks=weeks, days=days,
                               hours=hours, minutes=minutes, seconds=seconds,
                               firstweekday=firstweekday, now=now)


def dates_to_keep(dates,
                  years=0, months=0, weeks=0, days=0, firstweekday=SATURDAY,
                  now=None):
    """
    Return a set of dates that should be kept, out of ``dates``.

    See ``to_keep`` for a description of arguments.
    """
    datetimes = to_keep((datetime.combine(d, time()) for d in dates),
                        years=years, months=months, weeks=weeks, days=days,
                        hours=0, minutes=0, seconds=0,
                        firstweekday=firstweekday, now=now)
    return set(dt.date() for dt in datetimes)


def dates_to_delete(dates,
                    years=0, months=0, weeks=0, days=0, firstweekday=SATURDAY,
                    now=None):
    """
    Return a set of date that should be deleted, out of ``dates``.

    See ``to_keep`` for a description of arguments.
    """
    dates = set(dates)
    return dates - dates_to_keep(dates,
                                 years=years, months=months,
                                 weeks=weeks, days=days,
                                 firstweekday=firstweekday, now=now)
