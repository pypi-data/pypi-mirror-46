# -*- coding: utf-8 -*-

"""Tags to manipulate ttcal objects in templates.
"""
from __future__ import print_function
import traceback
from django import template
# from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def surround(ttval, n='1'):
    """Return values from ``ttval`` - ``n``
       up to (but not including) ``ttval`` + ``n``.
    """
    n = int(n, 10)
    cur = -n
    while cur < n:
        yield ttval + cur
        cur += 1


@register.filter
def chop_at_now(ttlist):
    """Chop the list of ttvalues at now.
    """
    ttlist = list(ttlist)
    if not ttlist:
        return []
    first = ttlist[0]
    now = first.__class__()
    return [ttval for ttval in ttlist if ttval <= now]


@register.filter
def previous(ttval, n='1'):
    """Return the previous `n` objects.
    """
    cur = ttval
    for _i in range(int(n, 10)):
        cur -= 1
        yield cur


@register.filter
def is_current(ttval):
    """Return True if the `ttval` is now.
    """
    print('is_current:', ttval, ttval == ttval.__class__())
    return ttval == ttval.__class__()
