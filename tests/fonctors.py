# -*- coding: utf-8 -*-

import unittest
from ADT.fonctors import *
from pipe import dedup, select

class BaseFonctorTest(unittest.TestCase):
    def assertFEqual(self, f1, f2):
        self.assertSequenceEqual(list(f1), list(f2))

class HelperFunctionsTest(BaseFonctorTest):
    def test_getattrsfromdict(self):
        def f(): pass
        class X:
            @property
            def p(self): pass
        attrs = public_attrs_fromdict({'i': 1, 'f':f, '_p':'xx', 'p': X.p})
        self.assertListEqual(list(attrs), ['i'])
        
    def test_getattrs_of_a_class(self):
        class X:
            i = 1
            f = 12.3
            s = "ss"
            x = None
            def m(self): pass
            @classmethod
            def cm(cls): pass
        self.assertListEqual( public_attrs(X), ["i", "f", "s", "x"] )

    def test_get_inherited_attrs_of_a_class(self):
        class Y:
            i = 1
            f = 12.3
        class X(Y):
            s = "ss"
            x = None
            def m(self): pass
        self.assertListEqual( public_attrs(X, True), ["i", "f", "s", "x"] )

    def test_getattrs_of_an_object(self):
        class X:
            i = 1
            f = 12.3
            s = "ss"
            x = None
            def m(self): pass
        x = X()
        self.assertListEqual( public_attrs(x), ["i", "f", "s", "x"] )

    def test_get_inherited_attrs_of_an_object(self):
        class Y:
            i = 1
            f = 12.3
        class X(Y):
            s = "ss"
            x = None
            def m(self): pass
        x = X()
        self.assertListEqual( public_attrs(x, True), ["i", "f", "s", "x"] )


    def test_to_iterable(self):
        import enum
        self.assertEqual(len(to_iterable(1)), 1)
        L = [1]
        self.assertEqual(len(to_iterable(L)), 1)
        self.assertEqual(len(to_iterable("ddd")), 1)
        B = enum.Enum('B', "dur mou")
        self.assertEqual(len(to_iterable(B)), 1)
    
class FonctorBaseTest(BaseFonctorTest):
    def test_base(self):
        # test all redondants are deleted
        self.assertFEqual(
            (1, 1, 2.2, 3, 4, 'aa', 'aa', None) | dedup,
            (1, 2.2, 3, 4, 'aa', None)
        )
    def test_fonctor(self):
        self.assertFEqual(
            ("a", "bb", "ccc") | select(lambda s: len(s)),
            (1,2,3)
        )

        
class FonctorClassTest(BaseFonctorTest):

    def test_valattrs(self):
        class X:
            x = 0
        class Y(X):
            i = 1
            f = 12.3
        y = Y(); y.i=12; y.f=3.0
        self.assertFEqual( y | valattrs(follow_mro=False), [12, 3.0] )
        self.assertFEqual( Y | valattrs(follow_mro=False), [1, 12.3] )
        self.assertFEqual( y | valattrs, [0, 12, 3.0] )
        self.assertFEqual( Y | valattrs, [0, 1, 12.3] )
        
    def test_FonctorClass(self):
        self.assertFEqual(
            (1,2.2,3,4,'a','abc',None,True) | CLASS | dedup,
            (int, float, str, type(None), bool)
        )
        self.assertFEqual(
            (1,2.2,3,4,'a') | CLASS | dedup,
            (int, float, str)
        )        

    def test_FonctorClass_old_newstyle_class(self):
        class X: pass
        class Y(object): pass
        x = X(); y = Y()
        self.assertFEqual(
            (x, y) | CLASS,
            (X, Y)
        )
        
    def test_FonctorAttr(self):
        f = (int, float) | attrs | dedup
        self.assertEqual(len(list(f)), 4)
        class X:
            A = 1
            B = 2
        class Y(X):
            C = 3
            D = 4
        f = Y | attrs
        self.assertFEqual(f, ['A', 'B', 'C', 'D'])
        f = Y | attrs(follow_mro=False)
        self.assertFEqual(f, ['C', 'D'])
        

    def test_Fonctor_CLASS_ATTR(self):
        f = (1,2.2,3,4,'a')| CLASS | attrs | dedup
        r = ('real', 'imag', 'numerator', 'denominator')
        self.assertFEqual(f, r)

    def test_FonctorObjectAttr(self):
        class X:
            A = 1
            B = 1.3
            C = 'abc'
            D = 1
        x = X()
        self.assertFEqual( x | valattrs,(1, 1.3, 'abc', 1))

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
        self.assertFEqual(
            (x, y1, y2) | valattrs(('A', 'D')),
            (1, 1, 12, 'x', 12, "zz")
        )
        
    def test_FonctorObjectAttr_CLASS(self):
        class X:
            A = 1
            B = 1.3
            C = 'abc'
            D = 1
        x = X()
        self.assertFEqual(
            x | valattrs | CLASS,
            (int, float, str, int)
        )

    def test_OBJOF(self):
        class X: pass
        class Y: pass
        class Z: pass
        x1 = X(); y = Y(); z = Z(); x2 = X()
        O = (x1, y, z, x2)
        self.assertFEqual(
            O | OBJOF(X, Y),
            (x1, y, x2)
        )
        self.assertFEqual(
            O | OBJOF(X),
            (x1, x2)
        )
        
    def test_Fonctor_without_hbds(self):
        class X: pass
        self.assertFEqual( X | attrs, [])
        self.assertFEqual( X() | CLASS, (X,))
        self.assertFEqual( X() | valattrs, [])

            
if __name__ == '__main__':
    unittest.main(
##        defaultTest=(
##            'FonctorClassTest.test_FonctorAttr'
##            ),
        verbosity=2,
        )
