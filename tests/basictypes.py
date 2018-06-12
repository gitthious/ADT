# -*- coding: utf-8 -*-

import unittest
from ADT.basictypes import *

class TestBasicMixin(unittest.TestCase):
    def test_positive(self):
        positive(12.1)
        positive(0)
        self.assertRaises(ValueError, positive, -1)

    def test_negative(self):
        negative(-12.3)
        negative(0)
        self.assertRaises(ValueError, negative, 1)

    def test_max_inclusive(self):
        r = MaxInclusive(10)
        r(9)
        r(10)
        self.assertRaises(ValueError, r,11)

    def test_min_max_inclusive(self):
        i = Interval(2, 10)
        i(2)
        i(10)
        i(5.4)
        self.assertRaises(ValueError, i, 1)
        self.assertRaises(ValueError, i, 11.3)

    def test_sized_string(self):
        r = SizedString(2)
        r("AB")
        with self.assertRaises(ValueError):
            r("ABC")

    def test_regex_string(self):
        r = Regex('[A-Z]*$')
        r("AAA")
        with self.assertRaises(ValueError):
            r("AeA")

    def test_subclassing(self):
        PosInt(12)
        with self.assertRaises(ValueError):
            PosInt('a')
        with self.assertRaises(ValueError):
            PosInt(-1)
            
if __name__ == '__main__':
    unittest.main() 
