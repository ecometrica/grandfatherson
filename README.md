Grandfatherson
==============

GrandFatherSon is a backup rotation calculator that implements the
[grandfather-father-son rotation scheme](http://en.wikipedia.org/wiki/Backup_rotation_scheme#Grandfather-father-son_backup).

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

    >>> from grandfatherson import dates_to_delete, SATURDAY
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

Installation
------------

The recommended way is to dowload from pypi with:

    pip install grandfatherson

Otherwise, run `python setup.py install` in your favorite virtualenv.

Contributing
------------

We will gladly review any pull requests submitted to our
[github repository](https://github.com/ecometrica/grandfatherson).

Testing
-------

All the tests are in (you'll never guess) test/. To execute them, simply
run the following:

    python run-tests.py

License
-------

grandfatherson is distributed under the BSD 3 clause lisence. See the
LICENSE file for more details.
