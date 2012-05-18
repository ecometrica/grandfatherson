from datetime import datetime
import unittest

from grandfatherson import (MONDAY, TUESDAY, WEDNESDAY, THURSDAY,
                            FRIDAY, SATURDAY, SUNDAY)
from grandfatherson.filters import (Seconds, Minutes, Hours, Days, Weeks,
                                    Months, Years)


class TestSeconds(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2000, 1, 1, 0, 0, 1, 1)
        self.datetimes = [
            datetime(2000, 1, 1, 0, 0, 1, 0),
            datetime(2000, 1, 1, 0, 0, 0, 1),
            datetime(2000, 1, 1, 0, 0, 0, 0),
            datetime(1999, 12, 31, 23, 59, 59, 999999),
            datetime(1999, 12, 31, 23, 59, 57, 0),
        ]

    def test_mask(self):
        self.assertEqual(
            Seconds.mask(datetime(1999, 12, 31, 23, 59, 59, 999999)),
            datetime(1999, 12, 31, 23, 59, 59, 0)
        )

    def test_future(self):
        datetimes = [datetime(2010, 1, 15, 0, 0, 0, 0)]  # Wikipedia
        self.assertEqual(Seconds.filter(datetimes, number=0, now=self.now),
                         set(datetimes))
        self.assertEqual(Seconds.filter(datetimes, number=1, now=self.now),
                         set(datetimes))

    def test_invalid_number(self):
        self.assertRaises(ValueError,
                          Seconds.filter, [], number=-1, now=self.now)
        self.assertRaises(ValueError,
                          Seconds.filter, [], number=0.1, now=self.now)
        self.assertRaises(ValueError,
                          Seconds.filter, [], number='1', now=self.now)

    def test_no_input(self):
        self.assertEqual(Seconds.filter([], number=1, now=self.now),
                         set())

    def test_no_results(self):
        self.assertEqual(Seconds.filter([self.now], number=0, now=self.now),
                         set())
        self.assertEqual(Seconds.filter(self.datetimes, number=0,
                                        now=self.now),
                         set())

    def test_current(self):
        self.assertEqual(Seconds.filter(self.datetimes, number=1,
                                        now=self.now),
                         set([datetime(2000, 1, 1, 0, 0, 1, 0)]))

    def test_duplicates(self):
        # Ensure we get the oldest per-second datetime when there are
        # duplicates: i.e. not datetime(2000, 1, 1, 0, 0, 0, 1)
        self.assertEqual(Seconds.filter(self.datetimes, number=2,
                                        now=self.now),
                         set([datetime(2000, 1, 1, 0, 0, 0, 0),
                              datetime(2000, 1, 1, 0, 0, 1, 0)]))

    def test_microseconds(self):
        self.assertEqual(Seconds.filter(self.datetimes, number=3,
                                        now=self.now),
                         set([datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0),
                              datetime(2000, 1, 1, 0, 0, 1, 0)]))

    def test_before_start(self):
        # datetime(1999, 12, 31, 23, 59, 57, 0) is too old to show up
        # in the results
        self.assertEqual(Seconds.filter(self.datetimes, number=4,
                                        now=self.now),
                         set([datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0),
                              datetime(2000, 1, 1, 0, 0, 1, 0)]))

    def test_all_input(self):
        self.assertEqual(Seconds.filter(self.datetimes, number=5,
                                        now=self.now),
                         set([datetime(1999, 12, 31, 23, 59, 57, 0),
                              datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0),
                              datetime(2000, 1, 1, 0, 0, 1, 0)]))

        self.assertEqual(Seconds.filter(self.datetimes, number=6,
                                        now=self.now),
                         set([datetime(1999, 12, 31, 23, 59, 57, 0),
                              datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0),
                              datetime(2000, 1, 1, 0, 0, 1, 0)]))


class TestMinutes(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2000, 1, 1, 0, 1, 1, 1)
        self.datetimes = [
            datetime(2000, 1, 1, 0, 1, 0, 0),
            datetime(2000, 1, 1, 0, 0, 1, 0),
            datetime(2000, 1, 1, 0, 0, 0, 0),
            datetime(1999, 12, 31, 23, 59, 59, 999999),
            datetime(1999, 12, 31, 23, 57, 0, 0),
        ]

    def test_mask(self):
        self.assertEqual(
            Minutes.mask(datetime(1999, 12, 31, 23, 59, 59, 999999)),
            datetime(1999, 12, 31, 23, 59, 0, 0)
        )

    def test_future(self):
        datetimes = [datetime(2010, 1, 15, 0, 0, 0, 0)]  # Wikipedia
        self.assertEqual(Minutes.filter(datetimes, number=0, now=self.now),
                         set(datetimes))
        self.assertEqual(Minutes.filter(datetimes, number=1, now=self.now),
                         set(datetimes))

    def test_invalid_number(self):
        self.assertRaises(ValueError,
                          Minutes.filter, [], number=-1, now=self.now)
        self.assertRaises(ValueError,
                          Minutes.filter, [], number=0.1, now=self.now)
        self.assertRaises(ValueError,
                          Minutes.filter, [], number='1', now=self.now)

    def test_no_input(self):
        self.assertEqual(Minutes.filter([], number=1, now=self.now),
                         set())

    def test_no_results(self):
        self.assertEqual(Minutes.filter([self.now], number=0, now=self.now),
                         set())
        self.assertEqual(Minutes.filter(self.datetimes, number=0,
                                        now=self.now),
                         set())

    def test_current(self):
        self.assertEqual(Minutes.filter(self.datetimes, number=1,
                                        now=self.now),
                         set([datetime(2000, 1, 1, 0, 1, 0, 0)]))

    def test_duplicates(self):
        # Ensure we get the oldest per-minute datetime when there are
        # duplicates: i.e. not datetime(2000, 1, 1, 0, 0, 1, 0)
        self.assertEqual(Minutes.filter(self.datetimes, number=2,
                                        now=self.now),
                         set([datetime(2000, 1, 1, 0, 0, 0, 0),
                              datetime(2000, 1, 1, 0, 1, 0, 0)]))

    def test_microseconds(self):
        self.assertEqual(Minutes.filter(self.datetimes, number=3,
                                        now=self.now),
                         set([datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0),
                              datetime(2000, 1, 1, 0, 1, 0, 0)]))

    def test_before_start(self):
        # datetime(1999, 12, 31, 23, 57, 0, 0) is too old to show up
        # in the results
        self.assertEqual(Minutes.filter(self.datetimes, number=4,
                                        now=self.now),
                         set([datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0),
                              datetime(2000, 1, 1, 0, 1, 0, 0)]))

    def test_all_input(self):
        self.assertEqual(Minutes.filter(self.datetimes, number=5,
                                        now=self.now),
                         set([datetime(1999, 12, 31, 23, 57, 0, 0),
                              datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0),
                              datetime(2000, 1, 1, 0, 1, 0, 0)]))

        self.assertEqual(Minutes.filter(self.datetimes, number=6,
                                        now=self.now),
                        set([datetime(1999, 12, 31, 23, 57, 0, 0),
                             datetime(1999, 12, 31, 23, 59, 59, 999999),
                             datetime(2000, 1, 1, 0, 0, 0, 0),
                             datetime(2000, 1, 1, 0, 1, 0, 0)]))


class TestHours(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2000, 1, 1, 1, 1, 1, 1)
        self.datetimes = [
            datetime(2000, 1, 1, 1, 0, 0, 0),
            datetime(2000, 1, 1, 0, 1, 0, 0),
            datetime(2000, 1, 1, 0, 0, 0, 0),
            datetime(1999, 12, 31, 23, 59, 59, 999999),
            datetime(1999, 12, 31, 21, 0, 0, 0),
        ]

    def test_mask(self):
        self.assertEqual(
            Hours.mask(datetime(1999, 12, 31, 23, 59, 59, 999999)),
            datetime(1999, 12, 31, 23, 0, 0, 0)
        )

    def test_future(self):
        datetimes = [datetime(2010, 1, 15, 0, 0, 0, 0)]  # Wikipedia
        self.assertEqual(Hours.filter(datetimes, number=0, now=self.now),
                         set(datetimes))
        self.assertEqual(Hours.filter(datetimes, number=1, now=self.now),
                         set(datetimes))

    def test_invalid_number(self):
        self.assertRaises(ValueError,
                          Hours.filter, [], number=-1, now=self.now)
        self.assertRaises(ValueError,
                          Hours.filter, [], number=0.1, now=self.now)
        self.assertRaises(ValueError,
                          Hours.filter, [], number='1', now=self.now)

    def test_no_input(self):
        self.assertEqual(Hours.filter([], number=1, now=self.now),
                         set())

    def test_no_results(self):
        self.assertEqual(Hours.filter([self.now], number=0, now=self.now),
                         set())
        self.assertEqual(Hours.filter(self.datetimes, number=0, now=self.now),
                         set())

    def test_current(self):
        self.assertEqual(Hours.filter(self.datetimes, number=1, now=self.now),
                         set([datetime(2000, 1, 1, 1, 0, 0, 0)]))

    def test_duplicates(self):
        # Ensure we get the oldest per-hour datetime when there are
        # duplicates: i.e. not datetime(2000, 1, 1, 0, 1, 0, 0)
        self.assertEqual(Hours.filter(self.datetimes, number=2,
                                        now=self.now),
                         set([datetime(2000, 1, 1, 0, 0, 0, 0),
                              datetime(2000, 1, 1, 1, 0, 0, 0)]))

    def test_microseconds(self):
        self.assertEqual(Hours.filter(self.datetimes, number=3, now=self.now),
                         set([datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0),
                              datetime(2000, 1, 1, 1, 0, 0, 0)]))

    def test_before_start(self):
        # datetime(1999, 12, 31, 21, 0, 0, 0) is too old to show up
        # in the results
        self.assertEqual(Hours.filter(self.datetimes, number=4, now=self.now),
                         set([datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0),
                              datetime(2000, 1, 1, 1, 0, 0, 0)]))

    def test_all_input(self):
        self.assertEqual(Hours.filter(self.datetimes, number=5, now=self.now),
                         set([datetime(1999, 12, 31, 21, 0, 0, 0),
                              datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0),
                              datetime(2000, 1, 1, 1, 0, 0, 0)]))

        self.assertEqual(Hours.filter(self.datetimes, number=6, now=self.now),
                         set([datetime(1999, 12, 31, 21, 0, 0, 0),
                              datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0),
                              datetime(2000, 1, 1, 1, 0, 0, 0)]))


class TestDays(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2000, 1, 1, 1, 1, 1, 1)
        self.datetimes = [
            datetime(2000, 1, 1, 1, 0, 0, 0),
            datetime(2000, 1, 1, 0, 0, 0, 0),
            datetime(1999, 12, 31, 23, 59, 59, 999999),
            datetime(1999, 12, 30, 0, 0, 0, 0),
            datetime(1999, 12, 28, 0, 0, 0, 0),
        ]

    def test_mask(self):
        self.assertEqual(
            Days.mask(datetime(1999, 12, 31, 23, 59, 59, 999999)),
            datetime(1999, 12, 31, 0, 0, 0, 0)
        )

    def test_future(self):
        datetimes = [datetime(2010, 1, 15, 0, 0, 0, 0)]  # Wikipedia
        self.assertEqual(Days.filter(datetimes, number=0, now=self.now),
                         set(datetimes))
        self.assertEqual(Days.filter(datetimes, number=1, now=self.now),
                         set(datetimes))

    def test_invalid_number(self):
        self.assertRaises(ValueError,
                          Days.filter, [], number=-1, now=self.now)
        self.assertRaises(ValueError,
                          Days.filter, [], number=0.1, now=self.now)
        self.assertRaises(ValueError,
                          Days.filter, [], number='1', now=self.now)

    def test_no_input(self):
        self.assertEqual(Days.filter([], number=1, now=self.now),
                         set())

    def test_no_results(self):
        self.assertEqual(Days.filter([self.now], number=0, now=self.now),
                         set())
        self.assertEqual(Days.filter(self.datetimes, number=0, now=self.now),
                         set())

    def test_current(self):
        self.assertEqual(Days.filter(self.datetimes, number=1, now=self.now),
                         set([datetime(2000, 1, 1, 0, 0, 0, 0)]))

    def test_duplicates(self):
        # Ensure we get the oldest per-day datetime when there are
        # duplicates: i.e. not datetime(2000, 1, 1, 1, 0, 0, 0)
        self.assertEqual(Days.filter(self.datetimes, number=2, now=self.now),
                         set([datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0)]))

    def test_before_start(self):
        # datetime(1999, 12, 28, 0, 0, 0, 0) is too old to show up
        # in the results
        self.assertEqual(Days.filter(self.datetimes, number=4, now=self.now),
                         set([datetime(1999, 12, 30, 0, 0, 0, 0),
                              datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0)]))

    def test_all_input(self):
        self.assertEqual(Days.filter(self.datetimes, number=5, now=self.now),
                         set([datetime(1999, 12, 28, 0, 0, 0, 0),
                              datetime(1999, 12, 30, 0, 0, 0, 0),
                              datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0)]))

        self.assertEqual(Days.filter(self.datetimes, number=6, now=self.now),
                         set([datetime(1999, 12, 28, 0, 0, 0, 0),
                              datetime(1999, 12, 30, 0, 0, 0, 0),
                              datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0)]))

    def test_leap_year(self):
        # 2004 is a leap year, because it is divisible by 4
        now = datetime(2004, 3, 1, 0, 0, 0, 0)
        datetimes_2004 = [
            datetime(2004, 3, 1, 0, 0, 0, 0),
            datetime(2004, 2, 29, 0, 0, 0, 0),
            datetime(2004, 2, 28, 0, 0, 0, 0),
            datetime(2004, 2, 27, 0, 0, 0, 0),
        ]

        self.assertEqual(Days.filter(datetimes_2004, number=1, now=now),
                         set([datetime(2004, 3, 1, 0, 0, 0, 0)]))

        self.assertEqual(Days.filter(datetimes_2004, number=2, now=now),
                         set([datetime(2004, 2, 29, 0, 0, 0, 0),
                              datetime(2004, 3, 1, 0, 0, 0, 0)]))

        self.assertEqual(Days.filter(datetimes_2004, number=3, now=now),
                         set([datetime(2004, 2, 28, 0, 0, 0, 0),
                              datetime(2004, 2, 29, 0, 0, 0, 0),
                              datetime(2004, 3, 1, 0, 0, 0, 0)]))

    def test_not_leap_year(self):
        # 1900 was not a leap year, because it is divisible by 400
        now = datetime(1900, 3, 1, 0, 0, 0, 0)
        datetimes_1900 = [
            datetime(1900, 3, 1, 0, 0, 0, 0),
            datetime(1900, 2, 28, 0, 0, 0, 0),
            datetime(1900, 2, 27, 0, 0, 0, 0),
        ]

        self.assertEqual(Days.filter(datetimes_1900, number=1, now=now),
                         set([datetime(1900, 3, 1, 0, 0, 0, 0)]))

        self.assertEqual(Days.filter(datetimes_1900, number=2, now=now),
                         set([datetime(1900, 2, 28, 0, 0, 0, 0),
                              datetime(1900, 3, 1, 0, 0, 0, 0)]))

        self.assertEqual(Days.filter(datetimes_1900, number=3, now=now),
                         set([datetime(1900, 2, 27, 0, 0, 0, 0),
                              datetime(1900, 2, 28, 0, 0, 0, 0),
                              datetime(1900, 3, 1, 0, 0, 0, 0)]))


class TestWeeks(unittest.TestCase):
    def setUp(self):
        # 1 January 2000 is a Saturday
        self.now = datetime(2000, 1, 1, 1, 1, 1, 1)
        self.datetimes = [
            datetime(2000, 1, 1, 1, 0, 0, 0),
            datetime(2000, 1, 1, 0, 0, 0, 0),
            datetime(1999, 12, 31, 23, 59, 59, 999999),
            datetime(1999, 12, 18, 0, 0, 0, 0),
            datetime(1999, 12, 4, 0, 0, 0, 0),
        ]

    def test_mask(self):
        # 31 December 1999 is a Friday.
        dt = datetime(1999, 12, 31, 23, 59, 59, 999999)
        self.assertEqual(dt.weekday(), FRIDAY)

        # Default firstweekday is Saturday
        self.assertEqual(Weeks.mask(dt),
                         Weeks.mask(dt, firstweekday=SATURDAY))
        self.assertEqual(Weeks.mask(dt),
                         datetime(1999, 12, 25, 0, 0, 0, 0))

        # Sunday
        self.assertEqual(Weeks.mask(dt, firstweekday=SUNDAY),
                         datetime(1999, 12, 26, 0, 0, 0, 0))

        # If firstweekday is the same as dt.weekday, then it should return
        # the same day.
        self.assertEqual(Weeks.mask(dt, firstweekday=dt.weekday()),
                         Days.mask(dt))

    def test_future(self):
        datetimes = [datetime(2010, 1, 15, 0, 0, 0, 0)]  # Wikipedia
        self.assertEqual(Weeks.filter(datetimes, number=0, now=self.now),
                         set(datetimes))
        self.assertEqual(Weeks.filter(datetimes, number=1, now=self.now),
                         set(datetimes))

    def test_invalid_number(self):
        self.assertRaises(ValueError,
                          Weeks.filter, [], number=-1, now=self.now)
        self.assertRaises(ValueError,
                          Weeks.filter, [], number=0.1, now=self.now)
        self.assertRaises(ValueError,
                          Weeks.filter, [], number='1', now=self.now)

    def test_no_input(self):
        self.assertEqual(Weeks.filter([], number=1, now=self.now),
                         set())

    def test_no_results(self):
        self.assertEqual(Weeks.filter([self.now], number=0, now=self.now),
                         set())
        self.assertEqual(Weeks.filter(self.datetimes, number=0, now=self.now),
                         set())

    def test_current(self):
        self.assertEqual(Weeks.filter(self.datetimes, number=1, now=self.now),
                         set([datetime(2000, 1, 1, 0, 0, 0, 0)]))

    def test_duplicates(self):
        # Ensure we get the oldest per-day datetime when there are
        # duplicates: i.e. not datetime(2000, 1, 1, 1, 0, 0, 0)
        self.assertEqual(Weeks.filter(self.datetimes, number=2, now=self.now),
                         set([datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0)]))

    def test_before_start(self):
        # datetime(1999, 12, 4, 0, 0, 0, 0) is too old to show up
        # in the results
        self.assertEqual(Weeks.filter(self.datetimes, number=4, now=self.now),
                         set([datetime(1999, 12, 18, 0, 0, 0, 0),
                              datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0)]))

    def test_all_input(self):
        self.assertEqual(Weeks.filter(self.datetimes, number=5, now=self.now),
                         set([datetime(1999, 12, 4, 0, 0, 0, 0),
                              datetime(1999, 12, 18, 0, 0, 0, 0),
                              datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0)]))

        self.assertEqual(Weeks.filter(self.datetimes, number=6, now=self.now),
                         set([datetime(1999, 12, 4, 0, 0, 0, 0),
                              datetime(1999, 12, 18, 0, 0, 0, 0),
                              datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0)]))


class TestMonths(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2000, 2, 1, 1, 1, 1, 1)
        self.datetimes = [
            datetime(2000, 2, 1, 0, 0, 0, 0),
            datetime(2000, 1, 1, 1, 0, 0, 0),
            datetime(2000, 1, 1, 0, 0, 0, 0),
            datetime(1999, 12, 31, 23, 59, 59, 999999),
            datetime(1999, 10, 1, 0, 0, 0, 0),
        ]

    def test_mask(self):
        self.assertEqual(
            Months.mask(datetime(1999, 12, 31, 23, 59, 59, 999999)),
            datetime(1999, 12, 1, 0, 0, 0, 0)
        )

    def test_future(self):
        datetimes = [datetime(2010, 1, 15, 0, 0, 0, 0)]  # Wikipedia
        self.assertEqual(Months.filter(datetimes, number=0, now=self.now),
                         set(datetimes))
        self.assertEqual(Months.filter(datetimes, number=1, now=self.now),
                         set(datetimes))

    def test_invalid_number(self):
        self.assertRaises(ValueError,
                          Months.filter, [], number=-1, now=self.now)
        self.assertRaises(ValueError,
                          Months.filter, [], number=0.1, now=self.now)
        self.assertRaises(ValueError,
                          Months.filter, [], number='1', now=self.now)

    def test_no_input(self):
        self.assertEqual(Months.filter([], number=1, now=self.now),
                         set())

    def test_no_results(self):
        self.assertEqual(Months.filter([self.now], number=0, now=self.now),
                         set())
        self.assertEqual(Months.filter(self.datetimes, number=0, now=self.now),
                         set())

    def test_current(self):
        self.assertEqual(Months.filter(self.datetimes, number=1, now=self.now),
                         set([datetime(2000, 2, 1, 0, 0, 0, 0)]))

    def test_duplicates(self):
        # Ensure we get the oldest per-month datetime when there are
        # duplicates: i.e. not datetime(2000, 1, 1, 1, 0, 0, 0)
        self.assertEqual(Months.filter(self.datetimes, number=2, now=self.now),
                         set([datetime(2000, 1, 1, 0, 0, 0, 0),
                              datetime(2000, 2, 1, 0, 0, 0, 0)]))

    def test_new_year(self):
        self.assertEqual(Months.filter(self.datetimes, number=3, now=self.now),
                         set([datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0),
                              datetime(2000, 2, 1, 0, 0, 0, 0)]))

    def test_before_start(self):
        # datetime(1999, 10, 1, 0, 0, 0, 0) is too old to show up
        # in the results
        self.assertEqual(Months.filter(self.datetimes, number=4, now=self.now),
                         set([datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0),
                              datetime(2000, 2, 1, 0, 0, 0, 0)]))

    def test_all_input(self):
        self.assertEqual(Months.filter(self.datetimes, number=5, now=self.now),
                         set([datetime(1999, 10, 1, 0, 0, 0, 0),
                              datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0),
                              datetime(2000, 2, 1, 0, 0, 0, 0)]))

        self.assertEqual(Months.filter(self.datetimes, number=6, now=self.now),
                         set([datetime(1999, 10, 1, 0, 0, 0, 0),
                              datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0),
                              datetime(2000, 2, 1, 0, 0, 0, 0)]))

    def test_multiple_years(self):
        now = datetime(2000, 1, 1, 0, 0, 0, 0)
        datetimes = [
            datetime(2000, 1, 1, 0, 0, 0, 0),
            datetime(1999, 12, 1, 0, 0, 0, 0),
            datetime(1999, 1, 1, 0, 0, 0, 0),
            datetime(1998, 12, 1, 0, 0, 0, 0),
            datetime(1997, 12, 1, 0, 0, 0, 0),
        ]

        # 12 months back ignores datetime(1999, 1, 1, 0, 0, 0, 0)
        self.assertEqual(Months.filter(datetimes, number=12, now=now),
                         set([datetime(1999, 12, 1, 0, 0, 0, 0),
                              datetime(2000, 1, 1, 0, 0, 0, 0)]))

        # But 13 months back gets it
        self.assertEqual(Months.filter(datetimes, number=13, now=now),
                         set([datetime(1999, 1, 1, 0, 0, 0, 0),
                              datetime(1999, 12, 1, 0, 0, 0, 0),
                              datetime(2000, 1, 1, 0, 0, 0, 0)]))

        # But 14 months back gets datetime(1998, 12, 1, 0, 0, 0, 0)
        self.assertEqual(Months.filter(datetimes, number=14, now=now),
                         set([datetime(1998, 12, 1, 0, 0, 0, 0),
                              datetime(1999, 1, 1, 0, 0, 0, 0),
                              datetime(1999, 12, 1, 0, 0, 0, 0),
                              datetime(2000, 1, 1, 0, 0, 0, 0)]))

        # As does 24 months back
        self.assertEqual(Months.filter(datetimes, number=24, now=now),
                         set([datetime(1998, 12, 1, 0, 0, 0, 0),
                              datetime(1999, 1, 1, 0, 0, 0, 0),
                              datetime(1999, 12, 1, 0, 0, 0, 0),
                              datetime(2000, 1, 1, 0, 0, 0, 0)]))

        # 36 months back should get datetime(1997, 12, 1, 0, 0, 0, 0)
        self.assertEqual(Months.filter(datetimes, number=36, now=now),
                         set([datetime(1997, 12, 1, 0, 0, 0, 0),
                              datetime(1998, 12, 1, 0, 0, 0, 0),
                              datetime(1999, 1, 1, 0, 0, 0, 0),
                              datetime(1999, 12, 1, 0, 0, 0, 0),
                              datetime(2000, 1, 1, 0, 0, 0, 0)]))


class TestYears(unittest.TestCase):
    def setUp(self):
        self.now = datetime(2000, 1, 1, 1, 1, 1, 1)
        self.datetimes = [
            datetime(2000, 1, 1, 1, 0, 0, 0),
            datetime(2000, 1, 1, 0, 0, 0, 0),
            datetime(1999, 12, 31, 23, 59, 59, 999999),
            datetime(1998, 1, 1, 0, 0, 0, 0),
            datetime(1996, 1, 1, 0, 0, 0, 0),
        ]

    def test_mask(self):
        self.assertEqual(
            Years.mask(datetime(1999, 12, 31, 23, 59, 59, 999999)),
            datetime(1999, 1, 1, 0, 0, 0, 0)
        )

    def test_future(self):
        datetimes = [datetime(2010, 1, 15, 0, 0, 0, 0)]  # Wikipedia
        self.assertEqual(Years.filter(datetimes, number=0, now=self.now),
                         set(datetimes))
        self.assertEqual(Years.filter(datetimes, number=1, now=self.now),
                         set(datetimes))

    def test_invalid_number(self):
        self.assertRaises(ValueError,
                          Years.filter, [], number=-1, now=self.now)
        self.assertRaises(ValueError,
                          Years.filter, [], number=0.1, now=self.now)
        self.assertRaises(ValueError,
                          Years.filter, [], number='1', now=self.now)

    def test_no_input(self):
        self.assertEqual(Years.filter([], number=1, now=self.now),
                         set())

    def test_no_results(self):
        self.assertEqual(Years.filter([self.now], number=0, now=self.now),
                         set())
        self.assertEqual(Years.filter(self.datetimes, number=0, now=self.now),
                         set())

    def test_current(self):
        self.assertEqual(Years.filter(self.datetimes, number=1, now=self.now),
                         set([datetime(2000, 1, 1, 0, 0, 0, 0)]))

    def test_duplicates(self):
        # Ensure we get the oldest per-month datetime when there are
        # duplicates: i.e. not datetime(2000, 1, 1, 1, 0, 0, 0)
        self.assertEqual(Years.filter(self.datetimes, number=2, now=self.now),
                         set([datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0)]))

    def test_before_start(self):
        # datetime(1996, 1, 1, 0, 0, 0, 0) is too old to show up
        # in the results
        self.assertEqual(Years.filter(self.datetimes, number=4, now=self.now),
                         set([datetime(1998, 1, 1, 0, 0, 0, 0),
                              datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0)]))

    def test_all_input(self):
        self.assertEqual(Years.filter(self.datetimes, number=5, now=self.now),
                         set([datetime(1996, 1, 1, 0, 0, 0, 0),
                              datetime(1998, 1, 1, 0, 0, 0, 0),
                              datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0)]))

        self.assertEqual(Years.filter(self.datetimes, number=6, now=self.now),
                         set([datetime(1996, 1, 1, 0, 0, 0, 0),
                              datetime(1998, 1, 1, 0, 0, 0, 0),
                              datetime(1999, 12, 31, 23, 59, 59, 999999),
                              datetime(2000, 1, 1, 0, 0, 0, 0)]))
