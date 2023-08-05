# -*- coding: utf-8 -*-
import re
import calendar
import datetime
from .day import Day, Days
from .week import Week
from .calfns import chop, rangecmp, rangetuple


class Month(object):
    """A calendar month.
    """

    month_name = ['', 'Januar', 'Februar', 'Mars', 'April', 'Mai', 'Juni',
                  'Juli', 'August', 'September', 'Oktober', 'November',
                  'Desember']
    year = None
    month = None

    @classmethod
    def from_idtag(cls, tag):
        """Parse idtag into `class`:Month.
        """
        # m20082
        y = int(tag[1:5])
        m = int(tag[5:])
        return cls(year=y, month=m)

    @classmethod
    def from_date(cls, d):
        """Create a Month from the date ``d``.
        """
        return cls(year=d.year, month=d.month)

    def rangetuple(self):
        return self.first.datetime(), (self.last + 1).datetime()

    @classmethod
    def parse(cls, txt):
        """Parse a textual representation into a Month object.
           Format YYYY-MM?
        """
        if not txt:
            return None

        mnth_matcher = re.compile(r"""
            (?P<year>\d{4})-?(?P<month>\d{1,2})
            """, re.VERBOSE)
        m = mnth_matcher.match(txt)
        if not m:
            raise ValueError(
                (u"Ugyldig format, må være åååå-mm, ikke %r." % txt).encode('u8'))
        mnth_groups = m.groupdict()

        return cls(int(mnth_groups["year"]), int(mnth_groups["month"]))

    def __init__(self, year=None, month=None, date=None):
        super(Month, self).__init__()
        if date is not None:
            self.year = date.year
            self.month = date.month
        elif year is month is date is None:
            td = datetime.date.today()
            self.year = td.year
            self.month = td.month
        else:
            assert None not in (year, month)
            self.year = year
            self.month = month

        if not (1 <= self.month <= 12):
            raise ValueError("Month must be in 1..12.")

        self.calendar = calendar.Calendar()
        self.name = self.month_name[self.month]
        self.short_name = self.name[:3]
        # self.short_name = calendar.month_abbr[self.month]
        self.weeks = [Week(days, self.month) for days in self._weeks()]
        # self.day = 1

    def __call__(self, daynum=None):
        """Return the given Day for this year.

           Usage::

               return ttcal.Year().december(23)

        """
        if daynum is None:  # pragma:nocover
            return self  # for when django tries to do value = value() *sigh*
        return Day(self.year, self.month, daynum)

    def __reduce__(self):
        """Deepcopy helper.
        """
        return Month, (self.year, self.month)

    def __unicode__(self):      # pragma: nocover
        return u"%04d-%02d" % (self.year, self.month)

    def __str__(self):      # pragma: nocover
        return '%04d-%02d' % (self.year, self.month)

    def __repr__(self):
        return 'Month(%s, %s)' % (self.year, self.month)

    # @property
    # def Year(self):
    #     """Return a Year object for the year-part of this month.
    #     """
    #     return Year(self.year)

    @property
    def Month(self):
        return self

    def __hash__(self):
        return self.year * 100 + self.month

    # def __eq__(self, other):
    #     noinspection PyBroadException
        # try:
        #     return self.year == other.year and self.month == other.month
        # except:
        #     return False

    def __len__(self):
        _, n = calendar.monthrange(self.year, self.month)
        return n

    def datetuple(self):
        """First date in month.
        """
        return self.year, self.month, 1

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

    def numdays(self):  # for use in template
        """The number of days in the month.
        """
        return len(self)

    def __add__(self, n):
        """Add n months to self.
        """
        me = self.year * 12 + (self.month - 1)
        me += n
        q, r = divmod(me, 12)
        return Month(q, r + 1)

    def __radd__(self, n):
        return self + n

    def __sub__(self, n):
        if isinstance(n, Month):
            first, last = min(self, n), max(self, n)
            ydiff = last.year - first.year
            mdiff = last.month - first.month
            res = 12 * ydiff + mdiff
            if self > n:
                return res
            return -res
        return self + (-n)

    # rsub doesn't make sense

    # NOTE: Django's query engine calls both __call__ and __iter__ on values
    #       that are passed in, and uses the return values instead of the value
    #       itself (i.e. with the implementation below, the queryset would get
    #       a list of Week objects instead of a Month object).
    # NB: W:\srv\venv\dev\Lib\site-packages\django\db\models\sql\where.py
    # NB: temp comment
    # NB:  if is_iterator(value):
    # NB:        # Consume any generators immediately, so that we can determine
    # NB:        # emptiness and transform any non-empty values correctly.
    # NB:        value = list(value)
    # def __iter__(self):
    #     return iter(self.weeks)

    def dayiter(self):
        for wk in iter(self.weeks):
            for day in wk:
                yield day

    def days(self):
        """Return a list of days (`class`:ttcal.Day) in this month.
        """
        res = []
        for wk in iter(self.weeks):
            for day in wk:
                if day.month == self.month:
                    res.append(day)  # yield day
        return res

    def idtag(self):
        """Return a text representation that is parsable by the from_idtag
           function (above), and is useable as part of an url.
        """
        return 'm%d%d' % (self.year, self.month)

    @property
    def daycount(self):
        """The number of days in this month (as an int).
        """
        n = calendar.mdays[self.month]
        if self.month == 2 and calendar.isleap(self.year):
            n += 1
        return n

    def prev(self):
        """Previous month.
        """
        return self - 1

    def next(self):
        """Next month.
        """
        return self + 1

    @property
    def first(self):
        """First day in month.
        """
        return Day(self.year, self.month, 1)

    @property
    def last(self):
        """Last day in month.
        """
        return Day(self.year, self.month, self.daycount)

    def _weeks(self):
        c = self.calendar
        return chop(c.itermonthdates(self.year, self.month), 7)

    def __contains__(self, date):
        return self.year == date.year and self.month == date.month

    def __getitem__(self, day):
        for wk in self.weeks:
            for d in wk:
                if d.compare(day) == 'day':
                    return d
        raise KeyError

    def mark(self, d, value='mark', method='replace'):
        try:
            day = self[d]
            if method == 'replace':
                day.mark = value
            elif method == 'append':
                if hasattr(day, 'mark'):
                    day.mark += value
                else:
                    day.mark = value

        except KeyError:  # pragma:nocover
            pass

    def marked_days(self):
        for wk in self.weeks:
            for d in wk:
                if hasattr(d, 'mark'):
                    yield d

    def _format(self, fmtchars):
        # http://blog.tkbe.org/archive/date-filter-cheat-sheet/
        for ch in fmtchars:
            if ch == 'y':
                yield str(self.year)[-2:]
            elif ch == 'Y':
                yield str(self.year)
            elif ch == 'n':
                yield str(self.month)
            elif ch == 'm':
                yield '%02d' % self.month
            elif ch == 'b':
                yield self.name[:3].lower()
            elif ch == 'M':
                yield self.name[:3]
            elif ch == 'N':
                # should be AP style, but doesn't make sense outside US.
                yield self.name[:3]
            elif ch == 'F':
                yield self.name
            else:
                yield ch

    def format(self, fmt=None):
        """Format according to format string. Default format is
           monthname, four-digit-year.
        """
        if fmt is None:
            fmt = "F, Y"
        tmp = list(self._format(list(fmt)))
        return ''.join(tmp)

    def range(self):
        """Return an iterator for the range of `self`.
        """
        # if hasattr(self, 'dayiter'):
        #     return self.dayiter()
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

    def timetuple(self):
        """Create timetuple from datetuple.
           (to interact with datetime objects).
        """
        d = datetime.date(*self.datetuple())
        t = datetime.time()
        return datetime.datetime.combine(d, t)


# noinspection PyPep8Naming
def _Month(self):
    """Return a Month object representing the month `self` belongs to.
    """
    return Month(self.year, self.month)
Day.Month = property(_Month)
