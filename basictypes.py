# -*- coding: utf-8 -*-

import re
from enum import Enum

# TODO: remplacer datetime par un module plus cohérent!
from datetime import time, timedelta
from datetime import datetime as pydatetime
from datetime import date as pydate
from dateutil import parser
# cf. https://pypi.org/project/colour/
import colour
from pathlib import Path

__all__ = [
    'Enum',
    'datetime', 'date', 'time', 'timedelta',
    'PosInt',
    'Percent',
    'MaxInclusive', 'Interval', 'MinExclusive', 'MaxExclusive', 'MinInclusive',
    'positive', 'negative',
    'Regex', 'SizedString',
    'Color',
    'Path',
    ]

            
class datetime(pydatetime):
    def __new__(cls, *args, **kargs):
        try:
            return parser.parse(*args, **kargs)
        except TypeError:
            return pydatetime.__new__(cls, *args, **kargs)
    
class date(pydate):
    def __new__(cls, *args, **kargs):
        d = parser.parse(*args, **kargs)
        d = pydate.__new__(cls, d.year, d.month, d.day)
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

class Color(colour.Color):
    @property
    def RGB(self):
        h = self.hex_l
        return int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16)



              
