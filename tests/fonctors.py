# -*- coding: utf-8 -*-

import unittest
from ADT.fonctors import *

class HelperFunctionsTest(unittest.TestCase):
    def test_getattrsfromdict(self):
        def f(): pass
        class X:
            @property
            def p(self): pass
        attrs = getattrsfromdict({'i': 1, 'f':f, '_p':'xx', 'p': X.p})
        self.assertListEqual(attrs, ['i'])
        
    def test_getattrs_of_a_class(self):
        class X:
            i = 1
            f = 12.3
            s = "ss"
            x = None
            def m(self): pass
            @classmethod
            def cm(cls): pass
        self.assertListEqual( getattrs(X), ["i", "f", "s", "x"] )

    def test_get_inherited_attrs_of_a_class(self):
        class Y:
            i = 1
            f = 12.3
        class X(Y):
            s = "ss"
            x = None
            def m(self): pass
        self.assertListEqual( getattrs(X, True), ["i", "f", "s", "x"] )

    def test_getattrs_of_an_object(self):
        class X:
            i = 1
            f = 12.3
            s = "ss"
            x = None
            def m(self): pass
        x = X()
        self.assertListEqual( getattrs(x), ["i", "f", "s", "x"] )

    def test_get_inherited_attrs_of_an_object(self):
        class Y:
            i = 1
            f = 12.3
        class X(Y):
            s = "ss"
            x = None
            def m(self): pass
        x = X()
        self.assertListEqual( getattrs(x, True), ["i", "f", "s", "x"] )

    def test_getvalattrs(self):
        class Y:
            i = 1
            f = 12.3
        y = Y(); y.i=12; y.f=3.0
        # Attention de ne pas oubier les ()!
        self.assertSetEqual( y | valattrs(), set([3.0, 12]) )
        self.assertSetEqual( Y | valattrs(), set([12.3, 1]) )

    def test_to_iterable(self):
        import enum
        self.assertEqual(len(to_iterable(1)), 1)
        L = [1]
        self.assertEqual(len(to_iterable(L)), 1)
        self.assertEqual(len(to_iterable("ddd")), 1)
        B = enum.Enum('B', "dur mou")
        self.assertEqual(len(to_iterable(B)), 1)
    
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
            (1,2.2,3,4,'a') | CLASS(),
            set((float, int, str))
        )        

    def test_FonctorClass_old_newstyle_class(self):
        class X: pass
        class Y(object): pass
        x = X(); y = Y()
        self.assertSetEqual(
            (x, y) | CLASS(),
            set((X, Y))
        )
        
    def test_FonctorAttr(self):
        f = (int, float) | attrs()
        self.assertEqual(len(f), 4)

    def test_Fonctor_CLASS_ATTR(self):
        f = (1,2.2,3,4,'a')| CLASS | attrs
        r = set(('denominator', 'real', 'numerator', 'imag'))
        self.assertSetEqual(f, r)

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

    def test_FonctorObjectNamedAttr(self):
        class X:
            A = 1
            B = 1.3
            C = 'abc'
            D = 1
        class Y:
            A = 12
            D = "x"
            Z = 23.3
        x = X(); y1 = Y(); y2 = Y(); y2.D = "zz"
        self.assertSetEqual(
            (x, y1, y2) | valattrs(('A', 'D')),
            set((1, 12, 'x', "zz"))
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

    def test_OBJOF(self):
        class X: pass
        class Y: pass
        class Z: pass
        x1 = X(); y = Y(); z = Z(); x2 = X()
        O = (x1, y, z, x2)
        self.assertSetEqual(
            O | OBJOF(X, Y),
            set((x1, y, x2))
        )
        self.assertSetEqual(
            O | OBJOF(X),
            set((x1, x2))
        )
        
    def test_Fonctor_without_hbds(self):
        class X: pass
        self.assertSetEqual( X | attrs, set())
        self.assertSetEqual( X() | CLASS, set((X,)))
        self.assertSetEqual( X() | valattrs, set())

    
if __name__ == '__main__':
    unittest.main(
##        defaultTest=(
##            'HelperFunctionsTest.test_getvalattrs'
##            )
        )
