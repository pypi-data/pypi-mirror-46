# -*- coding: utf-8 -*-
import datetime
from itertools import islice


def chop(it, n):
    """Chop iterator into `n` size chuchks.
    """
    while 1:
        s = list(islice(it, n))
        if not s:
            break
        yield s


def isoweek(year, week):
    """Iterate over the days in isoweek `week` of `year`.
    """
    # 4th of January is always in week 1
    wk1date = datetime.date(year, 1, 4)

    # daynumber of the 4th, zero-based
    weekday = wk1date.weekday()

    # (proleptic Gregorian) ordinal of first day of week 1
    day1 = wk1date.toordinal() - weekday

    # first day in week
    start = day1 + (week - 1) * 7
    # one past last day in week
    stop = day1 + week * 7

    for n in range(start, stop):
        yield datetime.date.fromordinal(n)


def rangetuple(x):
    if hasattr(x, 'rangetuple'):
        return x.rangetuple()
    if isinstance(x, datetime.date):
        return (datetime.datetime.combine(x, datetime.time()),
                datetime.datetime.combine(
                    datetime.date.fromordinal(1 + x.toordinal()), datetime.time())
                )
    return x


def rangecmp(interval_a, interval_b):
    """Compare half-open intervals [a, b) and [c, d)
       They compare equal if there is overlap.
    """
    (a, b) = interval_a
    (c, d) = interval_b
    if (a, b) == (c, d):
        return 0
    if (a, b) > (c, d):
        return -rangecmp((c, d), (a, b))

    if c < b < d:
        return 0
    if a < c < b:
        return 0
    if b <= c:
        return -1
    # the next if can never be reached, but kept for completeness.
    if b > c:  # pragma: nocover
        return 1
    raise ValueError(a, b, c, d)  # pragma: no cover
