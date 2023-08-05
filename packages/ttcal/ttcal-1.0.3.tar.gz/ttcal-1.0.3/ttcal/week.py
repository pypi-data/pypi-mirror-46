# -*- coding: utf-8 -*-
import datetime
from .day import Day, Days
from .calfns import isoweek, rangecmp, rangetuple


class Week(object):
    year = None
    num = None
    days = None
    month = None

    def range(self):
        """Return an iterator for the range of `self`.
        """
        return Days(self.first, self.last)

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

    @classmethod
    def from_idtag(cls, tag):
        # w20081
        y = int(tag[1:5])
        w = int(tag[5:])
        return cls.weeknum(w, y)

    @classmethod
    def weeknum(cls, n=None, year=None):
        if n is None and year is None:
            year, n = datetime.date.today().isocalendar()[:2]
        if year is None:
            year = datetime.date.today().year
        days = list(isoweek(year, n))
        month = days[0].month  # quite arbitrary
        return cls(days, month)

    def __init__(self, days, month):
        super(Week, self).__init__()
        # thursday is always in the correct iso-year per definition
        t = days[3].isocalendar()
        self.year = t[0]
        self.num = t[1]
        self.days = [Day(d, membermonth=month) for d in days]
        self.month = month

    @property
    def current(self):
        """True if today is in week.
        """
        return any(d.today for d in self.days)

    def idtag(self):
        return 'w%d%d' % (self.year, self.num)

    @property
    def first(self):
        """1st day of week.
        """
        return self.days[0]

    @property
    def last(self):
        """Last day of week.
        """
        return self.days[-1]

    def datetuple(self):
        """First day of this week.
        """
        return self.year, self.month, self.first.day

    def __str__(self):
        return 'Uke %d (%d)' % (self.num, self.year)

    def __repr__(self):
        return 'Week(%s, month=%s, year=%s)' % (self.num, self.month, self.year)

    def __iter__(self):
        return iter(self.days)

    def until_today(self):
        for d in self.days:
            if d.today:
                break
            yield d

    def __hash__(self):
        return self.year * 100 + self.num

    def rangetuple(self):
        return self.days[0].rangetuple()[0], self.days[-1].rangetuple()[-1]

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


        # t = (self.year, self.num)
        # if isinstance(other, Week):
        #     return cmp(t, (other.year, other.num))
        # if isinstance(other, Day):
        #     if self.days[-1] > other:
        #         return 1
        #     if self.days[0] < other:
        #         return -1
        #     return 0
        # if hasattr(other, 'year'):
        #     if self.year < other.year:
        #         return -1
        #     if self.year > other.year:
        #         return 1
        #     if hasattr(other, 'month'):
        #         if self.days[0] < other:
        #             return -1
        #         if self.days[-1] > other:
        #             return 1
        #         if hasattr(other, 'day'):
        #             if self.days[0] < other:
        #                 return -1
        #             if self.days[-1] > other:
        #                 return 1
        #             return 0
        # return 0

    # def __eq__(self, other):
    #     return self.year == other.year and self.num == other.num

    def __getitem__(self, n):
        return self.days[n]

    def __contains__(self, date):
        return date in self.days


# class Weeks(list):
#     def __init__(self, start, end):
#         super(Weeks, self).__init__()
#         assert start <= end
#         for i in range(start, end + 1):
#             self.append(Week.weeknum(i))
#
#     def range(self):
#         """Return an iterator for the range of `self`.
#         """
#         return self.dayiter()
#
#     def between_tuple(self):  # pylint:disable=E0213
#         """Return a tuple of datetimes that is convenient for sql
#            `between` queries.
#         """
#         return (self.first.datetime(),
#                 (self.last + 1).datetime() - datetime.timedelta(seconds=1))
#
#     @property
#     def middle(self):
#         """Return the day that splits the date range in half.
#         """
#         middle = (self.first.toordinal() + self.last.toordinal()) // 2
#         return Day.fromordinal(middle)
#
#     def timetuple(self):
#         """Create timetuple from datetuple.
#            (to interact with datetime objects).
#         """
#         d = datetime.date(*self.datetuple())
#         t = datetime.time()
#         return datetime.datetime.combine(d, t)
#
#     @property
#     def first(self):
#         """First day in first week.
#         """
#         return self[0][0]
#
#     @property
#     def last(self):
#         """Last day in last week.
#         """
#         return self[-1][-1]
#
#     def datetuple(self):
#         """First day of first week.
#         """
#         return self.first.datetuple()
#
#     def dayiter(self):
#         """Iterate over all days in all the weeks.
#         """
#         for wk in self:
#             for day in wk:
#                 yield day
#
#     def __repr__(self):
#         return '[' + ', '.join(map(str, iter(self))) + ']'


def _Week(self):
    """Return a Week object representing the week `self` belongs to.
    """
    return Week.weeknum(self.weeknum, self.isoyear)
Day.week = property(_Week)
