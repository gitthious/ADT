# -*- coding: utf-8 -*-

import unittest
from ADT.fonctors import *

def expected_fonctor(test, fonctor_result, expected_result):
    test.assertEqual(len(fonctor_result), len(expected_result))
    for o in expected_result:
        test.assertTrue(o in fonctor_result)
    test.assertEqual( len(fonctor_result.difference(expected_result)), 0)

class HelperFunctionsTest(unittest.TestCase):
    def test_getattrsfromdict(self):
        def f(): pass
        attrs = getattrsfromdict({'i': 1, 'f':f, '_p':'xx'})
        self.assertEqual( len(attrs), 1)
        for attr in attrs:
            self.assertIn( attr, ["i", ])
        
    def test_getattrs_of_a_class(self):
        class X:
            i = 1
            f = 12.3
            s = "ss"
            x = None
            def m(self): pass
            @classmethod
            def cm(cls): pass
        attrs = getattrs(X)
        self.assertEqual( len(attrs), 4)
        for attr in attrs:
            self.assertIn( attr, ["i", "f", "s", "x"])

    def test_getattrs_of_an_object(self):
        class X:
            i = 1
            f = 12.3
            s = "ss"
            x = None
            def m(self): pass
        x = X()
        attrs = getattrs(x)
        self.assertEqual( len(attrs), 4)
        for attr in attrs:
            self.assertIn( attr, ["i", "f", "s", "x"])
    
class FonctorBaseTest(unittest.TestCase):
    def test_base(self):
        r = [1, 2.2, 3, 4, 'aa', None] # fonctor is a set(), then all redondants are deleted
        f = (1, 1, 2.2, 3, 4, 'aa', 'aa', None) | IDENT
        expected_fonctor(self, f, r)
    def test_fonctor(self):
        f = ("a", "bb", "ccc") | Fonctor(len)
        r = (1, 2, 3)
        expected_fonctor(self, f, r)
        
class FonctorClassTest(unittest.TestCase):
                
    def test_FonctorClass(self):
        r = (float, bool, int, str, type(None))
        f = (1,2.2,3,4,'a','abc',None,True) | CLASS
        expected_fonctor(self, f, r)
        
        r = (float, int, str)
        f = (1,2.2,3,4,'a') | CLASS
        expected_fonctor(self, f, r)

    def test_FonctorClass_old_newstyle_class(self):
        class X: pass
        class Y(object): pass
        x = X(); y = Y()
        r = (X, Y)
        f = (x, y) | CLASS
        expected_fonctor(self, f, r)
        
    def test_FonctorAttr(self):
        f = (int, float) | ATT
        self.assertEqual(len(f), 4)

    def test_Fonctor_CLASS_ATTR(self):
        f = (1,2.2,3,4,'a')| CLASS | ATT 
        self.assertEqual(len(f), 4)

    def test_FonctorObjectAttr(self):
        class X:
            A = 1
            B = 1.3
            C = 'abc'
            D = 1
        x = X()
        f = x | OATT
        r = (1, 1.3, 'abc')
        expected_fonctor(self, f, r)
        
    def test_FonctorObjectAttr_CLASS(self):
        class X:
            A = 1
            B = 1.3
            C = 'abc'
            D = 1
        x = X()
        f = x | OATT | CLASS
        r = (int, float, str)
        expected_fonctor(self, f, r)

    def test_Fonctor_without_hbds(self):
        class X: pass
        expected_fonctor(self, X | ATT, [])
        expected_fonctor(self, X() | CLASS, (X,))
        expected_fonctor(self, X() | OATT, [])

if __name__ == '__main__':
    unittest.main() 
