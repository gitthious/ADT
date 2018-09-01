# -*- coding: utf-8 -*-

import unittest
from ADT.fonctors import *

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
        # fonctor is a set(), then all redondants are deleted
        self.assertSetEqual(
            (1, 1, 2.2, 3, 4, 'aa', 'aa', None) | IDENT,
            set((1, 2.2, 3, 4, 'aa', None))
        )
    def test_fonctor(self):
        self.assertSetEqual(
            ("a", "bb", "ccc") | Fonctor(len),
            set((1,2,3))
        )
        
class FonctorClassTest(unittest.TestCase):
                
    def test_FonctorClass(self):
        self.assertSetEqual(
            (1,2.2,3,4,'a','abc',None,True) | CLASS,
            set((float, bool, int, str, type(None)))
        )
        self.assertSetEqual(
            (1,2.2,3,4,'a') | CLASS,
            set((float, int, str))
        )        

    def test_FonctorClass_old_newstyle_class(self):
        class X: pass
        class Y(object): pass
        x = X(); y = Y()
        self.assertSetEqual(
            (x, y) | CLASS,
            set((X, Y))
        )
        
    def test_FonctorAttr(self):
        f = (int, float) | attrs
        self.assertEqual(len(f), 4)

    def test_Fonctor_CLASS_ATTR(self):
        f = (1,2.2,3,4,'a')| CLASS | attrs 
        self.assertEqual(len(f), 4)

    def test_FonctorObjectAttr(self):
        class X:
            A = 1
            B = 1.3
            C = 'abc'
            D = 1
        x = X()
        self.assertSetEqual(
            x | valattrs,
            set((1, 1.3, 'abc'))
        )
        
    def test_FonctorObjectAttr_CLASS(self):
        class X:
            A = 1
            B = 1.3
            C = 'abc'
            D = 1
        x = X()
        self.assertSetEqual(
            x | valattrs | CLASS,
            set((int, float, str))
        )

    def test_Fonctor_without_hbds(self):
        class X: pass
        self.assertSetEqual( X | attrs, set())
        self.assertSetEqual( X() | CLASS, set((X,)))
        self.assertSetEqual( X() | valattrs, set())

if __name__ == '__main__':
    unittest.main() 
