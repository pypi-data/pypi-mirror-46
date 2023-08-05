# -*- coding: utf-8 -*-
"""Date (single day) operations.
"""
import calendar
import datetime
import re
import six
from .calfns import rangecmp, rangetuple
from .duration import Duration


class fstr(str):
    """String sub-class with a split() method that splits a given indexes.

       Usage::
          >>> from __future__ import print_function
          >>> r = fstr('D2008022002')
          >>> print(r.split(1, 5, 7, 9))
          ['D', '2008', '02', '20', '02']
          >>> _, year, _ = r.split(1,5)
          >>> year
          '2008'

    """

    def split(self, *ndxs):
        if len(ndxs) == 0:
            return [self]
        if len(ndxs) == 1:
            i = ndxs[0]
            return [self[:i], self[i:]]

        res = []
        b = 0
        while ndxs:
            a, b, ndxs = b, ndxs[0], ndxs[1:]
            res.append(self[a:b])
        res.append(self[b:])

        return res


class Day(datetime.date):
    """A calendar date.
    """

    day_name = u'''mandag tirsdag onsdag torsdag fredag
                   lørdag søndag'''.split()

    day_code = "M U W H F A S".split()

    def __reduce__(self):
        return Day, (self.year, self.month, self.day)

    def __int__(self):
        return self.toordinal()

    @classmethod
    def from_idtag(cls, tag):
        """Return Day from idtag.
        """
        if len(tag) == 9:
            # d2008022002
            y, m, d = map(int, fstr(tag).split(1, 5, 7)[1:])
            return cls(y, m, d, membermonth=m)
        else:
            # d2008022002
            y, m, d, b = map(int, fstr(tag).split(1, 5, 7, 9)[1:])
            return cls(y, m, d, membermonth=b)

    @classmethod
    def parse(cls, strval):
        """Parse date value from a string.  Allowed syntax include
           ::

               yyyy-mm-dd, yyyy-m-dd, yyyy-mm-d, yyyy-m-d
               dd-mm-yyyy, etc.
               dd/mm/yyyy, ...
               dd.mm.yyyy, ...
               ddmmyyyy

        """
        if not strval or not strval.strip():
            # strval is None or contains only spaces
            return None

        datere = re.compile(r"""
            (?:\s*)
            (?P<isodate>
              (?P<iso_yr>[12]\d{3})
              (?P<sep>[-./\s])
              (?P<iso_mnth>0[1-9]|1[012]|[1-9])
              (?P=sep)
              (?P<iso_day>3[01]|[12]\d|0[1-9]|[1-9]))
            |(?P<dmy>
              (?P<dmy_day>3[01]|[12]\d|0[1-9]|\d)
              (?P<dmy_sep>[-./\s])
              (?P<dmy_mnth>0[1-9]|1[012]|\d)
              (?P=dmy_sep)
              (?P<dmy_yr>[12]\d{3}))
            |(?P<nsp>
              (?P<nsp_day>3[01]|[12]\d|0[1-9])
              (?P<nsp_mnth>0[1-9]|1[012])
              (?P<nsp_yr>[12]\d{3}))
            |(?P<isonsp>
              (?P<isonsp_yr>20[1-5]\d)
              (?P<isonsp_mnth>0[1-9]|1[012])
              (?P<isonsp_day>3[01]|[12]\d|0[1-9]))
            |(?P<two>
              (?P<two_day>3[01]|[12]\d|0[1-9]|\d)
              (?P<two_sep>[./\s])
              (?P<two_mnth>0[1-9]|1[012]|\d)
              (?P=two_sep)
              (?P<two_yr>[1-9]\d))
            (?:\s*)
        """, re.VERBOSE)
        m = datere.match(strval)
        if not m:
            raise ValueError("Cannot parse %r as date." % strval)
        prefix = ''

        g = m.groupdict()
        if g['isodate']:
            prefix = 'iso'

        elif g['dmy']:
            prefix = 'dmy'

        elif g['nsp']:
            prefix = 'nsp'

        elif g['isonsp']:
            prefix = 'isonsp'

        elif g['two']:
            prefix = 'two'

        day, month, year = [int(g['%s_%s' % (prefix, val)])
                            for val in ['day', 'mnth', 'yr']]

        if year < 13:
            raise ValueError("Cannot parse %r as date." % strval)
        if year < 100:
            year += 2000

        return cls(year, month, day)

    def __new__(cls, *args, **kw):
        if len(args) == 3:
            y, m, d = args
        elif len(args) == 1:
            t = args[0]
            y, m, d = t.year, t.month, t.day
        elif len(args) == 0:
            t = datetime.date.today()
            y, m, d = t.year, t.month, t.day
        else:
            raise TypeError('incorrect number of arguments')

        obj = super(Day, cls).__new__(cls, y, m, d)
        obj.membermonth = kw.get('membermonth', obj.month)
        return obj

    @staticmethod
    def get_day_name(daynum, length=None):
        """Return dayname for daynum.
        """
        if length is None:
            return Day.day_name[daynum]
        else:
            return Day.day_name[daynum][:length]

    def range(self):
        """Return an iterator for the range of `self`.
        """
        return Days(self.first, self.last)

    def rangetuple(self):
        return self.datetime(), (self+1).datetime()

    def between_tuple(self):
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

    def __hash__(self):
        return hash('%04s%02s%02s' % (self.year, self.month, self.day))

    def __repr__(self):
        return '%d-%d-%d-%d' % (self.year, self.month, self.day,
                                self.membermonth)

    def __unicode__(self):
        return u'%04d-%02d-%02d' % (self.year, self.month, self.day)

    def __str__(self):  # pragma:nocover
        if six.PY2:
            return self.__unicode__().encode('u8')
        elif six.PY3:
            return self.__unicode__()

    def datetime(self, hour=0, minute=0, second=0):
        """Extend `self` to datetime.
        """
        return datetime.datetime(self.year, self.month, self.day,
                                 hour, minute, second)

    def date(self):
        """Excplicitly convert to datetime.date.
        """
        return datetime.date(self.year, self.month, self.day)

    def datetuple(self):
        """Return year, month, day.
        """
        return self.year, self.month, self.day

    def __add__(self, n):
        return Day.fromordinal(self.toordinal() + n)

    # make first and last properties, because
    # self.first = self.last = self creates too many cycles :-)
    @property
    def first(self):
        """Define self == self.first for polymorphic usage with other classes.
        """
        return self

    @property
    def last(self):
        """Define self == self.last for polymorphic usage with other classes.
        """
        return self

    def next(self):
        """Return Tomorrow (for use in templates).
        """
        return self + 1

    def prev(self):
        """Return Yesterday (for use in templates).
        """
        return self - 1

    def __sub__(self, x):
        """Return number of days between Days or Day n days ago.
        """
        if isinstance(x, Day):
            return self.toordinal() - x.toordinal()
        elif isinstance(x, Duration):
            return Day.fromordinal(self.toordinal() - x.days)
        elif isinstance(x, six.integer_types):
            return Day.fromordinal(self.toordinal() - x)
        else:
            raise ValueError('Wrong operands for subtraction: %s and %s'
                             % (type(self), type(x)))

    @property
    def dayname(self):
        """The semi-localized name of self.
        """
        return self.day_name[self.weekday]

    @property
    def code(self):
        """One letter code representing the dayname.
        """
        return self.day_code[self.weekday]

    @property
    def weeknum(self):
        """Return the isoweek of `self`.
        """
        return self.isocalendar()[1]

    @property
    def isoyear(self):
        """Return the `isoyear` of `self`.
        """
        return self.isocalendar()[0]

    # week, Month, and Year, are added later (don't uncomment them here, since
    # that leads to nasty circular dependencies.
    #
    # @property
    # def week(self):
    #     """Return a Week object representing the week `self` belongs to.
    #     """
    #     from .week import Week
    #     return Week.weeknum(self.weeknum, self.isoyear)

    # @property
    # def Month(self):
    #     """Return a Month object representing the month `self` belongs to.
    #     """
    #     from .month import Month
    #     return Month(self.year, self.month)

    # @property
    # def Year(self):
    #     """Return a Year object representing the year `self` belongs to.
    #     """
    #     from .year import Year
    #     return Year(self.year)

    @property
    def display(self):
        """Return the 'class' of self.
        """
        res = set()
        if self.today and (self.membermonth == self.month):
            res.add('today')
        if self.in_month:
            res.add('month')
        else:
            res.add('noday')
        if self.weekend:
            res.add('weekend')
        if hasattr(self, 'mark'):
            res.add(self.mark)

        return ' '.join(res)

    @property
    def idtag(self):
        """Return the idtag for `self`: dyyyymmddmm.
        """
        return 'd%d%02d%02d%02d' % (self.year, self.month, self.day,
                                    self.membermonth)

    @property
    def today(self):
        """True if self is today.
        """
        return self.compare(datetime.date.today()) == 'day'

    @property
    def weekday(self):
        """True if self is a weekday.
        """
        return calendar.weekday(self.year, self.month, self.day)

    @property
    def weekend(self):
        """True if self is Saturday or Sunday.
        """
        return 5 <= self.weekday <= 6

    @property
    def special(self):
        """True if the database has an entry for this date (sets special_hours).
        """
        return False

    @property
    def in_month(self):
        """True iff the day is in its month.
        """
        return self.month == self.membermonth

    def compare(self, other):
        """Return how similar self is to other, i.e. the smallest factor
           they have in common ('day', 'month', or 'year').
           Returns None if the Days are in different years.
        """
        if not hasattr(other, 'year'):
            return None
        if self.year == other.year:
            if self.month == other.month:
                if self.day == other.day:
                    return 'day'
                else:
                    return 'month'
            else:
                return 'year'
        else:
            return None

    def _format(self, fmtchars):
        # http://blog.tkbe.org/archive/date-filter-cheat-sheet/
        simplefmt = {
            'y': lambda: str(self.year)[-2:],
            'Y': lambda: str(self.year),
            'W': lambda: str(self.weeknum),
            'w': lambda: str(self.weekday),
            'n': lambda: str(self.month),
            'm': lambda: '%02d' % self.month,
            'b': lambda: self.Month.format('b'),
            'M': lambda: self.Month.format('M'),
            'N': lambda: self.Month.format('N'),
            'F': lambda: self.Month.format('F'),
            'j': lambda: str(self.day),
            'd': lambda: '%02d' % self.day,
            'D': lambda: self.dayname[:3],
            'l': lambda: self.dayname,
            'z': lambda: str(int(self) - int(Day(self.year, 1, 1))),
        }
        ch = ""
        for ch in fmtchars:
            yield simplefmt.get(ch, lambda: ch)()

    def format(self, fmt=None):
        """Emulate Django's date filter.
        """
        if fmt is None:
            # pylint:disable=C0301
            # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-DATE_FORMAT
            fmt = "N j, Y"
        tmp = list(self._format(list(fmt)))
        return ''.join(tmp)

    def timetuple(self):
        """Create timetuple from datetuple.
           (to interact with datetime objects).
        """
        d = datetime.date(*self.datetuple())
        t = datetime.time()
        return datetime.datetime.combine(d, t)

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


class Today(Day):
    """Special subclass for today's date.
    """
    def __new__(cls, *args, **kw):
        t = datetime.date.today()
        y, m, d = t.year, t.month, t.day
        obj = super(Today, cls).__new__(cls, y, m, d)
        obj.membermonth = obj.month
        return obj

    today = True


class Days(list):
    """A contigous set of days.
    """

    def __init__(self, start, end, start_week=False):
        super(Days, self).__init__()
        assert start <= end
        if start_week:
            start = start - start.weekday  # set to monday

        for i in range(start.toordinal(), end.toordinal() + 1):
            self.append(Day.fromordinal(i))

    @property
    def first(self):
        """1st day
        """
        return self[0]

    @property
    def last(self):
        """last day
        """
        return self[-1]

    def range(self):
        """Return an iterator for the range of `self`.
        """
        return Days(self.first, self.last)

    def between_tuple(self):
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
