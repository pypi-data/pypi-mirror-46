# -*- coding: utf-8 -*-
"""Extension of datetime.timedelta.
"""
import datetime
import re


class Duration(datetime.timedelta):
    """A duration of time.
    """

    @classmethod
    def sum(cls, sequence, start=None):
        """Return the sum of sequence.
           (built-in sum only works with numbers).
        """
        if start is None:
            start = cls(0)
        res = start
        for item in sequence:
            res += item
        return res

    @classmethod
    def parse(cls, txt):
        """Parse a textual representation into a Duration object.
           Format HHH:MM:SS.
        """
        if not txt:
            return None

        time_matcher = re.compile(r"""
            (?:
                (?P<negation>-)
            )?
            (?:
                (?P<weeks>\d+) \W* (?:weeks?|w),?
            )?
            \W*
            (?:
                (?P<days>\d+) \W* (?:days?|d),?
            )?
            \W*
            (?:
                (?P<hours>\d+):
                (?P<minutes>\d+)
                (?::(?P<seconds>\d+)
                (?:\.(?P<microseconds>\d+))?)?
            )?
            """, re.VERBOSE)
        time_matches = time_matcher.match(txt)
        time_groups = time_matches.groupdict()
        keys = list(time_groups.keys())

        if time_groups.get('negation') == '-':
            scale = -1
            keys.remove('negation')
        else:
            scale = 1

        for key in keys:
            time_groups[key] = int(time_groups[key]) if time_groups[key] else 0
        time_groups["days"] = time_groups["days"] + (time_groups["weeks"] * 7)

        res = cls(
            days=time_groups["days"],
            hours=time_groups["hours"],
            minutes=time_groups["minutes"],
            seconds=time_groups["seconds"])

        return res * scale

    def __new__(cls, *args, **kw):
        if len(args) == 1 and isinstance(args[0], datetime.timedelta):
            years = 0
            days = args[0].days
            hours = 0
            minutes = 0
            seconds = args[0].seconds

        else:
            years = kw.get('years', 0)
            days = kw.get('days', 0)
            hours = kw.get('hours', 0)
            minutes = kw.get('minutes', 0)
            seconds = kw.get('seconds', 0)

        # an average year is 365.2425 days..
        leap_days = int(365.2425 * years - 365 * years)
        obj = super(Duration, cls).__new__(cls,
                                           days=days + years * 365,
                                           hours=hours + leap_days,
                                           minutes=minutes,
                                           seconds=seconds)
        return obj

    def __repr__(self):
        dt = self.duration_tuple()
        return '%sDuration(hours=%d, minutes=%d, seconds=%d)' % dt

    def duration_tuple(self):
        """Return self as hours, minutes, seconds.
        """
        seconds = self.toint()
        sign = -1 if seconds < 0 else 1
        seconds *= sign
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return '-' if sign < 0 else '', hours, minutes, seconds

    @property
    def hrs(self):
        """The number of hours in self.
        """
        sgn, hr, _mn, _sc = self.duration_tuple()
        return int(sgn == "") * hr

    @property
    def mins(self):
        """The number of minutes in self.
        """
        sgn, _hr, mn, _sc = self.duration_tuple()
        return int(sgn == "") * mn

    @property
    def secs(self):
        """The number of seconds in self.
        """
        sgn, _hr, _mn, sc = self.duration_tuple()
        return int(sgn == "") * sc

    def __str__(self):      # pragma: nocover
        return '%s%d:%02d:%02d' % self.duration_tuple()

    def __unicode__(self):      # pragma: nocover
        return u'%s%d:%02d:%02d' % self.duration_tuple()

    def toint(self):
        """Convert self to integer.
        """
        return self.seconds + 3600 * 24 * self.days

    __hash__ = datetime.timedelta.__hash__

    def __eq__(self, other):
        if hasattr(other, '__req__'):
            return other.__req__(self)

        if isinstance(other, datetime.timedelta):
            return super(Duration, self).__eq__(other)

        # if isinstance(other, Duration):
        #     return self.duration_tuple() == other.duration_tuple()

        if isinstance(other, int) and other == 0:
            return self.toint() == 0

        return False

    def __ne__(self, other):
        if hasattr(other, '__rne__'):
            return other.__rne__(self)

        if isinstance(other, datetime.timedelta):
            return super(Duration, self).__ne__(other)

        # if isinstance(other, Duration):
        #     return self.duration_tuple() != other.duration_tuple()

        if isinstance(other, int) and other == 0:
            return self.toint() != 0

        return False

    def __lt__(self, other):
        if hasattr(other, '__rlt__'):
            return other.__rlt__(self)
        if isinstance(other, datetime.timedelta):
            return super(Duration, self).__lt__(other)
        if hasattr(other, 'toint'):
            return self.toint() < other.toint()
        return False

    def __le__(self, other):
        if hasattr(other, '__rle__'):
            return other.__rle__(self)
        if isinstance(other, datetime.timedelta):
            return super(Duration, self).__le__(other)
        if hasattr(other, 'toint'):
            return self.toint() <= other.toint()
        return False

    def __gt__(self, other):
        if hasattr(other, '__rgt__'):
            return other.__rgt__(self)
        if isinstance(other, datetime.timedelta):
            return super(Duration, self).__gt__(other)
        if isinstance(other, int):
            return self.toint() > other
        if hasattr(other, 'toint'):
            return self.toint() > other.toint()
        return False

    def __ge__(self, other):
        if hasattr(other, '__rge__'):
            return other.__rge__(self)
        if isinstance(other, datetime.timedelta):
            return super(Duration, self).__ge__(other)
        if hasattr(other, 'toint'):
            return self.toint() >= other.toint()
        return False

    def __mul__(self, other):
        return Duration(super(Duration, self).__mul__(other))

    def __add__(self, other):
        return Duration(super(Duration, self).__add__(other))

    def __sub__(self, other):
        return Duration(super(Duration, self).__sub__(other))

    def __div__(self, other):       # pragma: nocover
        # this one is called for Python 2.7
        if isinstance(other, Duration):
            try:
                return float(self.toint()) / float(other.toint())
            except ZeroDivisionError:
                return 0.0
        return Duration(super(Duration, self).__div__(other))

    def __truediv__(self, other):   # pragma: nocover
        # this one is used for Python 3+
        if isinstance(other, Duration):
            try:
                return int(float(self.toint()) / float(other.toint()))
            except ZeroDivisionError:
                return 0
        return Duration(super(Duration, self).__truediv__(other))

    # def __rsub__(self, other):
    #     return other.__sub__(self)
    #
    # def __rmul__(self, other):
    #     return other.__mul__(self)
    #
    # def __rfloordiv__(self, other):
    #     return other.__floordiv__(self)
    #
    # def __rdiv__(self, other):
    #     return other.__div__(self)
    #
    # def __radd__(self, other):
    #     return other.__add__(self)
