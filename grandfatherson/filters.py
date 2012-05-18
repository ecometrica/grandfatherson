"""
Filters used by GrandFatherSon to decide which datetimes to keep.
"""

import calendar
from datetime import date, datetime, time, timedelta


class Filter(object):
    """Base class."""

    @classmethod
    def mask(cls, dt, **options):
        """
        Return a datetime with the same value as ``dt``, keeping only
        significant values.
        """
        raise NotImplemented

    @classmethod
    def start(cls, now, number, **options):
        """
        Return the starting datetime: ``number`` of units before ``now``.
        """
        return (cls.mask(now, **options) -
                timedelta(**{cls.__name__.lower(): number - 1}))

    @classmethod
    def filter(cls, datetimes, number, now=None, **options):
        """Return a set of datetimes, after filtering ``datetimes``.

        The result will be the ``datetimes`` which are ``number`` of
        units before ``now``, until ``now``, with approximately one
        unit between each of them.  The first datetime for any unit is
        kept, later duplicates are removed.

        If there are ``datetimes`` after ``now``, they will be
        returned unfiltered.
        """
        if number < 0 or not isinstance(number, (int, long)):
            raise ValueError('Invalid number: %s' % number)

        if now is None:
            now = datetime.now()
        if not hasattr(now, 'second'):
            # now looks like a date, so convert it into a datetime
            now = datetime.combine(now, time(23, 59, 59, 999999))

        # Always keep datetimes from the future
        future = set(dt for dt in datetimes if dt > now)

        if number == 0:
            return future

        # Don't consider datetimes from before the start
        start = cls.start(now, number, **options)
        valid = (dt for dt in datetimes if start <= dt <= now)

        # Deduplicate datetimes with the same mask() value by keeping
        # the oldest.
        kept = {}
        for dt in sorted(valid):
            kept.setdefault(cls.mask(dt), dt)

        return set(kept.values()) | future


class Seconds(Filter):
    @classmethod
    def mask(cls, dt, **options):
        """
        Return a datetime with the same value as ``dt``, to a
        resolution of seconds.
        """
        return dt.replace(microsecond=0)


class Minutes(Filter):
    @classmethod
    def mask(cls, dt, **options):
        """
        Return a datetime with the same value as ``dt``, to a
        resolution of minutes.
        """
        return dt.replace(second=0, microsecond=0)


class Hours(Filter):
    @classmethod
    def mask(cls, dt, **options):
        """
        Return a datetime with the same value as ``dt``, to a
        resolution of hours.
        """
        return dt.replace(minute=0, second=0, microsecond=0)


class Days(Filter):
    @classmethod
    def mask(cls, dt, **options):
        """
        Return a datetime with the same value as ``dt``, to a
        resolution of days.
        """
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)


class Weeks(Filter):
    DAYS_IN_WEEK = 7

    @classmethod
    def start(cls, now, number, firstweekday=calendar.SATURDAY, **options):
        """
        Return the starting datetime: ``number`` of weeks before ``now``.

        ``firstweekday`` determines when the week starts. It defaults
        to Saturday.
        """
        week = cls.mask(now, firstweekday=firstweekday, **options)
        days = (number - 1) * cls.DAYS_IN_WEEK
        return week - timedelta(days=days)

    @classmethod
    def mask(cls, dt, firstweekday=calendar.SATURDAY, **options):
        """
        Return a datetime with the same value as ``dt``, to a
        resolution of weeks.

        ``firstweekday`` determines when the week starts. It defaults
        to Saturday.
        """
        correction = (dt.weekday() - firstweekday) % cls.DAYS_IN_WEEK
        week = dt - timedelta(days=correction)
        return week.replace(hour=0, minute=0, second=0, microsecond=0)


class Months(Filter):
    MONTHS_IN_YEAR = 12

    @classmethod
    def start(cls, now, number, **options):
        """
        Return the starting datetime: ``number`` of months before ``now``.
        """
        year = now.year
        month = now.month - number + 1
        # Handle negative months
        if month < 0:
            year = year + (month / cls.MONTHS_IN_YEAR)
            month = month % cls.MONTHS_IN_YEAR
        # Handle December
        if month == 0:
            year = year - 1
            month = 12
        return cls.mask(now, **options).replace(year=year, month=month)

    @classmethod
    def mask(cls, dt, **options):
        """
        Return a datetime with the same value as ``dt``, to a
        resolution of months.
        """
        return dt.replace(day=1,
                          hour=0, minute=0, second=0, microsecond=0)


class Years(Filter):
    @classmethod
    def start(cls, now, number, **options):
        """
        Return the starting datetime: ``number`` of years before ``now``.
        """
        return cls.mask(now).replace(year=(now.year - number + 1))

    @classmethod
    def mask(cls, dt, **options):
        """
        Return a datetime with the same value as ``dt``, to a
        resolution of years.
        """
        return dt.replace(month=1, day=1,
                          hour=0, minute=0, second=0, microsecond=0)
