# -*- coding: utf-8 -*-
from builtins import str
import datetime
from .calfns import chop, rangecmp, rangetuple
from .day import Days, Day
from .month import Month


# noinspection PyPep8Naming
class Year(object):
    def __init__(self, year=None):
        super(Year, self).__init__()
        if year is None:
            year = datetime.date.today().year
        self.year = year
        self.months = [Month(year, i + 1) for i in range(12)]

    def __int__(self):
        return self.year

    def range(self):
        """Return an iterator for the range of `self`.
        """
        return self.dayiter()

    def rangetuple(self):
        return self.first.datetime(), (self+1).first.datetime()

    def __lt__(self, other):
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) < 0

    def __le__(self, other):
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) <= 0

    def __eq__(self, other):
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) == 0

    def __gt__(self, other):
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) > 0

    def __ge__(self, other):
        othr = rangetuple(other)
        if othr is other:
            return False
        return rangecmp(self.rangetuple(), othr) >= 0

    def timetuple(self):
        d = datetime.date(*self.first.datetuple())
        t = datetime.time()
        return datetime.datetime.combine(d, t)

    def between_tuple(self):  # pylint:disable=E0213
        """Return a tuple of datetimes that is convenient for sql
           `between` queries.
        """
        return (self.first.datetime(),
                (self.last + 1).datetime() - datetime.timedelta(seconds=1))

    @property
    def middle(self):
        """Return the day that splits the date range in half.
        """
        middle = (self.first.toordinal() + self.last.toordinal()) // 2
        return Day.fromordinal(middle)

    # def timetuple(self):
    #     """Create timetuple from datetuple.
    #        (to interact with datetime objects).
    #     """
    #     d = datetime.date(*self.datetuple())
    #     t = datetime.time()
    #     return datetime.datetime.combine(d, t)

    def __unicode__(self):      # pragma: nocover
        return str(self.year)

    def __repr__(self):
        return 'Year(%d)' % self.year

    def __str__(self):      # pragma: nocover
        return str(self.year)

    @property
    def Month(self):
        """For orthogonality in the api.
        """
        return self.months[0]

    @property
    def Year(self):
        return self

    @classmethod
    def from_idtag(cls, tag):
        """Year tags have the lower-case letter y + the four digit year,
           eg. y2008.
        """
        y = int(tag[1:5])
        return cls(year=y)

    def idtag(self):
        """Year tags have the lower-case letter y + the four digit year,
           eg. y2008.
        """
        return 'y%d' % self.year

    def marked_days(self):
        for m in self.months:
            for day in m.marked_days():
                yield day

    def datetuple(self):
        """January 1.
        """
        return self.year, None, None

    def __add__(self, n):
        """Add n years to self.
        """
        return Year(self.year + n)

    def __radd__(self, n):
        return self + n

    def __sub__(self, n):
        return self + (-n)

    # rsub doesn't make sense

    def prev(self):
        """Previous year.
        """
        return self - 1

    def next(self):
        """Next year.
        """
        return self + 1

    @property
    def H1(self):
        """First half of this year.
        """
        return self.months[:6]

    @property
    def H2(self):
        """Last half of this year.
        """
        return self.months[6:]

    def halves(self):
        """Both halves of the year.
        """
        return [self.H1, self.H2]

    @property
    def Q1(self):
        """1st quarter.
        """
        return self.months[:3]

    @property
    def Q2(self):
        """2nd quarter.
        """
        return self.months[3:6]

    @property
    def Q3(self):
        """3rd quarter.
        """
        return self.months[6:9]

    @property
    def Q4(self):
        """4th quarter.
        """
        return self.months[9:]

    def quarters(self):
        """Every quarter in this year.
        """
        return [self.Q1, self.Q2, self.Q3, self.Q4]

    # pylint:disable=C0111
    @property
    def january(self):
        return self.months[0]

    @property
    def february(self):
        return self.months[1]

    @property
    def march(self):
        return self.months[2]

    @property
    def april(self):
        return self.months[3]

    @property
    def may(self):
        return self.months[4]

    @property
    def june(self):
        return self.months[5]

    @property
    def july(self):
        return self.months[6]

    @property
    def august(self):
        return self.months[7]

    @property
    def september(self):
        return self.months[8]

    @property
    def october(self):
        return self.months[9]

    @property
    def november(self):
        return self.months[10]

    @property
    def december(self):
        return self.months[11]
    # pylint:enable=C0111

    def dayiter(self):
        for m in self.months:
            for d in m.days():
                yield d

    def rows(self):
        return chop(iter(self.months), 3)

    def rows4(self):
        return chop(iter(self.months), 4)

    @property
    def first(self):
        """First day of first month.
        """
        return self.months[0].first

    @property
    def last(self):
        """Last day of last month.
        """
        return self.months[-1].last

    def __hash__(self):
        return self.year

    # def __eq__(self, other):
    #     if hasattr(other, 'year'):
    #         return self.year == other.year
    #     return False

    def __contains__(self, date):
        return date.year == self.year

    def __getitem__(self, day):
        m = self.months[day.month - 1]
        return m[day]

    def mark_period(self, p, value='mark'):
        d = p.first
        while d != p.last:
            self.mark(d, value)
            d += 1
        self.mark(p.last, value)

    def mark(self, d, value='mark'):
        try:
            self[d].mark = value
        except KeyError:  # pragma:nocover
            pass

    def _format(self, fmtchars):
        # http://blog.tkbe.org/archive/date-filter-cheat-sheet/
        for ch in fmtchars:
            if ch == 'y':
                yield str(self.year)[-2:]
            elif ch == 'Y':
                yield str(self.year)
            else:
                yield ch

    def format(self, fmt=None):
        """Format according to format string. Default format is
           monthname, four-digit-year.
        """
        if fmt is None:
            fmt = "Y"
        tmp = list(self._format(list(fmt)))
        return ''.join(tmp)


# noinspection PyPep8Naming
def _Day_Year(self):
    """Return a Year object representing the year `self` belongs to.
    """
    return Year(self.year)
Day.Year = property(_Day_Year)


# noinspection PyPep8Naming
def _Month_Year(self):
    """Return a Year object for the year-part of this month.
    """
    return Year(self.year)
Month.Year = property(_Month_Year)
