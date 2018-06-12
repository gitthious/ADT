# -*- coding: utf-8 -*-

import enum, re
from datetime import datetime, date, time, timedelta

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
    
# cf. https://stackoverflow.com/questions/4828080/how-to-make-an-immutable-object-in-python
##class immutable(object):
##    def __init__(self, immutable_params):
##        self.immutable_params = immutable_params
##
##    def __call__(self, new):
##        params = self.immutable_params
##
##        def __set_if_unset__(self, name, value):
##            if name in self.__dict__:
##                raise Exception("Attribute %s has already been set" % name)
##
##            if not name in params:
##                raise Exception("Cannot create atribute %s" % name)
##
##            self.__dict__[name] = value;
##
##        def __new__(cls, *args, **kws):
##            cls.__setattr__ = __set_if_unset__
##
##            return super(cls.__class__, cls).__new__(cls, *args, **kws)
##
##        return __new__

##class Point(object):
##    @immutable(['x', 'y'])
##    def __new__(): pass
##
##    def __init__(self, x, y):
##        self.x = x
##        self.y = y
##
##class Point(tuple):
##    __slots__ = []
##    def __new__(cls, x, y):
##        return tuple.__new__(cls, (x, y))
##    @property
##    def x(self):
##        return tuple.__getitem__(self, 0)
##    @property
##    def y(self):
##        return tuple.__getitem__(self, 1)
##    def __getitem__(self, item):
##        raise TypeError

# https://en.wikipedia.org/wiki/Immutable_object#Python
##import collections
##Point = collections.namedtuple('Point', ['x', 'y'])

# A voir: annotations en python (typage?)
# https://stackoverflow.com/questions/4204075/assignment-in-python

##class Unit:
##    pass
