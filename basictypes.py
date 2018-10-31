# -*- coding: utf-8 -*-

from enum import Enum
import re
# TODO: remplacer datetime par un module plus cohérent!
from datetime import date, time, timedelta
from datetime import datetime as pydatetime

__all__ = [
    'Enum',
    'datetime', 'date', 'time', 'timedelta',
    'PosInt',
    'Percent',
    'MaxInclusive', 'Interval', 'MinExclusive', 'MaxExclusive', 'MinInclusive',
    'positive', 'negative',
    'Regex', 'SizedString',
    
    ]

class datetime(pydatetime):
    def __new__(cls, *args, **kargs):
        d = args[0]
        if isinstance(d, str):
            try:
                d = cls.strptime(d, "%Y%m%dT%H%M%S")
            except ValueError:
                try:
                    d = cls.strptime(d, "%Y-%m-%dT%H:%M:%S")
                except ValueError:
                    try:
                        d = cls.strptime(d, "%Y-%m-%dT%H:%M:%SZ")
                    except ValueError:
                        d = cls.strptime(d, "%Y-%m-%d %H:%M:%S")
            d = pydatetime.__new__(cls, d.year, d.month, d.day,
                                   d.hour, d.minute, d.second)
        elif isinstance(d, pydatetime):
            d = pydatetime.__new__(cls, d.year, d.month, d.day, d.hour,
                                   d.minute, d.second, d.microsecond, d.tzinfo)
        else:
            d = pydatetime.__new__(cls, *args, **kargs)
        return d
            


class MaxInclusive:
    def __init__(self, max_value):
        self.max = max_value
    def __call__(self, value):
        if value > self.max:
            raise ValueError("Expected <= %s, not %s" % (str(self.max), str(value)))
    
class MinExclusive(object):
    def __init__(self, min_value):
        self.min = min_value
    def __call__(self, value):
        if value <= self.min:
            raise ValueError("Expected > %s, not %s" % (str(self.min), str(value)))

class MaxExclusive(MaxInclusive):
    def __call__(self, value):
        if value >= self.max:
            raise ValueError("Expected < %s, not %s" % (str(self.max), str(value)))

class MinInclusive(MinExclusive):
    def __call__(self, value):
        if value < self.min:
            raise ValueError("Expected >= %s, not %s" % (str(self.min), str(value)))

positive = MinInclusive(0)
negative = MaxInclusive(0)        

class PosInt(int):
            def __new__(cls, *args, **kargs):
                v = int.__new__(cls, *args, **kargs)
                positive(v)
                return v
            
class SizedString(object):
    def __init__(self, maxlen):
        self.maxlen = maxlen
    def __call__(self, value):
        if len(value) > self.maxlen:
            raise ValueError("Expected len = %s, not %s" % (str(self.maxlen), str(value)))
        
class Regex(object):
    def __init__(self, pattern):
        self.pattern = pattern
        self.compiled_pattern = re.compile(pattern)
    def __call__(self, value):
        if not self.compiled_pattern.match(value):
            raise ValueError("Invalid value '%s' don't match with pattern '%s'" \
                             % (str(value), self.pattern))

class Interval(MinInclusive, MaxInclusive):
    def __init__(self, mininc, maxinc):
        MinInclusive.__init__(self, mininc)
        MaxInclusive.__init__(self, maxinc)
    def __call__(self, value):
        MinInclusive.__call__(self, value)
        MaxInclusive.__call__(self, value)


class Percent(float):
    def __new__(cls, *args, **kargs):
        v = float.__new__(cls, *args, **kargs)
        interval = Interval(0,1)
        interval(v)
        return v






              
