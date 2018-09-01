# -*- coding: utf-8 -*-

import unittest
from ADT.basictypes import Enum, date, datetime
from ADT.fonctors import CLASS
from ADT.hbds import *
from ADT import units

class AttTest(unittest.TestCase):

    def test_create(self):
        A = Att()
        self.assertIsNone(A.name)

        A = Att(default=1)
        self.assertIs(A.type, int)

    def test_validate(self):
        A = Att(int)
        self.assertIsNone(A._validate(None))
        self.assertEqual(A._validate(1), 1)
        self.assertEqual(A._validate('1'), 1)
        with self.assertRaises(TypeError):
            A._validate("t")
    
    def test_get(self):
        class X:
            A = Att(int, 1)
        self.assertEqual(X.A.name, 'A')
        x = X()
        self.assertEqual(x.A, 1)
        self.assertNotIn('A', x.__dict__)

    def test_inheritance_get(self):
        class Y:
            A = Att(int, 1)
        class X(Y): pass
        self.assertEqual(X.A.name, 'A')
        x = X()
        self.assertEqual(x.A, 1)
        self.assertNotIn('A', x.__dict__)
        # manque le cas où l'exception KeyError peut survenir

    def test_set(self):
        class X:
            A = Att(int)
        x = X()

        x.A = 12
        self.assertEqual(x.A, 12)

        x.A = "120"
        self.assertEqual(x.A, 120)

        with self.assertRaises(TypeError):
            x.A = "t"
            
        # impossible to control this without rewrite 
        # __setattr__() of X class!
        X.A = 2.3 # It would be better to prevent this
        self.assertEqual(X.A, 2.3)

    def test_set_with_type(self):
        class XT(type):
            A = Att()
            def __new__(cls, clsname, bases, clsdict):
                clsobj = type.__new__(cls, clsname, bases, clsdict)
                return clsobj        
        class X(metaclass=XT): pass
        class Y(metaclass=XT): pass
        X.A = 1; Y.A = 2
        self.assertEqual(X.A, 1)
        self.assertEqual(Y.A, 2)
        
    def test_constraint(self):
        def non_zero(value):
            if value == 0:
                raise ValueError("0 unexpected")
        A = Att(constraint=non_zero)
        with self.assertRaises(ValueError):
            A._validate(0)

    def test_doc(self):
        # not tested
        pass

    def test_mandatory(self):
        # not tested
        pass

class CreateAttTest(unittest.TestCase):
        
    def test_no_vals(self):
        a = create_Att()
        self.assertIsNone(a.type)
        self.assertIsNone(a.default)
        self.assertFalse(a.mandatory)
        self.assertIsNone(a.doc)
        self.assertIsNone(a.constraint)
        self.assertIsNone(a.unit)

    def test_type(self):
        a = create_Att(int)
        self.assertIs(a.type, int)
        self.assertIsNone(a.default)
        self.assertFalse(a.mandatory)
        self.assertIsNone(a.doc)
        self.assertIsNone(a.constraint)
        self.assertIsNone(a.unit)

    def test_default(self):
        a = create_Att(12.3)
        self.assertIs(a.type, float)
        self.assertEqual(a.default, 12.3)
        self.assertFalse(a.mandatory)
        self.assertIsNone(a.doc)
        self.assertIsNone(a.constraint)
        self.assertIsNone(a.unit)

    def test_mandatory(self):
        a = create_Att(Att.required)
        self.assertIsNone(a.type)
        self.assertIsNone(a.default)
        self.assertTrue(a.mandatory)
        self.assertIsNone(a.doc)
        self.assertIsNone(a.constraint)
        self.assertIsNone(a.unit)

    def test_unit(self):
        a = create_Att(units.Meter.metre)
        self.assertIsNone(a.type)
        self.assertIsNone(a.default)
        self.assertFalse(a.mandatory)
        self.assertIsNone(a.doc)
        self.assertIsNone(a.constraint)
        self.assertIs(a.unit, units.Meter.metre)

    def test_Att(self):
        a = Att()
        A = create_Att(a)
        self.assertIs(a, A)

    def test_all_vals(self):
        different_orders = (
            (int, 12, Att.required, units.Meter.metre),
            (int, 12, units.Meter.metre, Att.required),
            (int, Att.required, 12, units.Meter.metre),
            (int, Att.required, units.Meter.metre, 12),
            (int, units.Meter.metre, 12, Att.required),
            (int, units.Meter.metre, Att.required, 12),

            (12, int, Att.required, units.Meter.metre),
            (12, int, units.Meter.metre, Att.required),
            (12, Att.required, int, units.Meter.metre),
            (12, Att.required, units.Meter.metre, int),
            (12, units.Meter.metre, int, Att.required),
            (12, units.Meter.metre, Att.required, int),

            (Att.required, 12, int, units.Meter.metre),
            (Att.required, 12, units.Meter.metre, int),
            (Att.required, int, 12, units.Meter.metre),
            (Att.required, int, units.Meter.metre, 12),
            (Att.required, units.Meter.metre, 12, int),
            (Att.required, units.Meter.metre, int, 12),

            (units.Meter.metre, 12, Att.required, int),
            (units.Meter.metre, 12, int, Att.required),
            (units.Meter.metre, Att.required, 12, int),
            (units.Meter.metre, Att.required, int, 12),
            (units.Meter.metre, int, 12, Att.required),
            (units.Meter.metre, int, Att.required, 12),
            )
        for a,b,c,d in different_orders:
            a = create_Att(a,b,c,d)
            self.assertIs(a.type, int)
            self.assertEqual(a.default, 12)
            self.assertIs(a.mandatory, Att.required)
            self.assertIsNone(a.doc)
            self.assertIsNone(a.constraint)
            self.assertIs(a.unit, units.Meter.metre)

    def test_errors(self):
        with self.assertRaises(TypeError):
            create_Att(int, 1, Att.required, units.Meter.metre, int)
            
        with self.assertRaises(TypeError):
            create_Att(Att(), Att())

        with self.assertRaises(TypeError):
            create_Att(ComposedAtt(), Att())

##class AttTest(unittest.TestCase):
##    def setUp(self):
##        class XType(Class):
##            A = Att(str, "xx")
##        @strict
##        class X(metaclass=XType):
##            b = int
##        self.X = X
##        @strict
##        class Y(metaclass=XType):
##            pass
##        self.Y = Y
##        
##    def test_set(self):
####        x = self.X()
####        x.b = 1
####        print(self.X.A)
##        self.assertEqual( self.X.A, "xx")
##        self.assertEqual( self.Y.A, "xx")
##        self.X.A = "xxxx"
##        self.assertEqual( self.X.A, "xxxx")
##        self.Y.A = "yyyy"
##        self.assertEqual( self.Y.A, "yyyy")
##        # test a 2nd time to test a bug if Att is a class variable
##        self.assertEqual( self.X.A, "xxxx")
##
##    def test_fonctor_ATT(self):
##        A = self.X | ATT
##        self.assertSetEqual(A, set(['A', 'b']))
##        A = self.Y | ATT
##        self.assertSetEqual(A, set(['A']))

        
class ClassAndAttrTest(unittest.TestCase):
    def setUp(self):
        E = Enum('E', "a b c")
        class X(metaclass=Class):
            i = Att(int)
            f = Att(float, 1.2)
            s = Att(str)
            x = Att()
            e = Att(E, E.a)
            dt = Att(datetime, datetime(2018, 8, 7))
            def m(self): pass
        self.E = E
        self.X = X

    def test_getattrs_class(self):
        attrs = getattrs(self.X)
        self.assertEqual( len(attrs), 6)
        for attr in attrs:
            self.assertIn( attr, ["i", "f", "s", "x", "e", "dt"])

    def test_get_undefined_att(self):
        x = self.X()
        with self.assertRaises(AttributeError):
            getattr(x, 'b')

    def test_get_unset_att(self):
        x = self.X()
        self.assertIs(x.i,None)
        
    def test_get_att_default_value(self):
        x = self.X()
        self.assertEqual(x.f,1.2)
        self.assertEqual(x.e, self.E.a)

    def test_set_att(self):
        x = self.X()
        x.i = 12
        self.assertEqual(x.i,12)

    def test_set_att_with_subtyped_value(self):
        x = self.X()
        class STR(str): pass
        x.s = STR("AAA")
        self.assertEqual(x.s,"AAA")

    def test_set_att_to_none(self):
        x = self.X()
        x.i = None
        self.assertIs(x.i,None)

    def test_set_untyped_att(self):
        x = self.X()
        x.x = self.X
        self.assertIs(x.x,self.X)

    def test_set_att_vith_bad_typed_value(self):
        x = self.X()
        with self.assertRaises(TypeError):
            x.i = "aa"
        with self.assertRaises(TypeError):
            x.dt = date(2018, 8, 10)

    def test_att_constraint(self):
        def non_zero(value):
            if value == 0:
                raise ValueError("0 unexpected")
        class X(metaclass=Class):
            A = Att(constraint=non_zero)
        x = X()
        with self.assertRaises(ValueError):
            x.A = 0
        try:
            x.A = 0
        except ValueError as e:
            self.assertEqual(str(e), "0 unexpected")
            
            
    def test_att_type(self):
        self.assertIs(self.X.i.type, int)
        self.assertIs(self.X.f.type, float)
        x = self.X(1, 1.2, "test")
        self.assertIs(type(x.i), int)
        self.assertIs(type(x.f), float)
        self.assertIs(type(x.s), str)
        self.assertIs(type(x.x), type(None))
        
    def test_instance_type(self):
        self.assertIs(type(self.X()), self.X )

    def test_class_type(self):
        self.assertIs(type(self.X), Class)

    def test_init_method(self):
        x = self.X(1, s="test", f=5.3)
        self.assertEqual(x.i, 1)
        self.assertEqual(x.f, 5.3)
        self.assertEqual(x.s, "test")
        self.assertIs(x.x, None)

    def test_init_method_with_bad_args(self):
        with self.assertRaises(TypeError):
            self.X(f="test", i=5.3, s=12)

    def test_init_method_with_mandatory_att(self):
        class Y(metaclass=Class):
            a = Att(mandatory=True)
            b = Att()
            c = Att(str, "test", mandatory=True)

        y = Y(12, 13, "test2")
        self.assertEqual(y.a, 12)
        self.assertEqual(y.b, 13)
        self.assertEqual(y.c, "test2")
        
    def test_init_method_with_bad_ordered_mandatory_att(self):
        with self.assertRaises(SyntaxError):
            class Y(metaclass=Class):
                a = Att(mandatory=True)
                c = Att()
                b = Att(str, mandatory=True)

##        def test_user_defined_init(self):
##            pass

    def test_class_with_no_attribute(self):
        class Y(metaclass=Class):
            pass
        self.assertEqual( len(getattrs(Y)), 0)
        
    def test_set_undeclared_att(self):
        with self.assertRaises(AttributeError):
            self.X().z = 12
        
        with self.assertRaises(AttributeError):
            self.X.z = 12
                                
    def test_att_heritance(self):
        class Y(self.X): pass
        y = Y()
        self.assertIsNone(y.i)
        
class ComposedAttTest(unittest.TestCase):
    def setUp(self):
        class X:
            ca = ComposedAtt(
                a = Att(int),
                b = (float, 12.5),
                c = str,
            )
        self.x = X()

    def test_basic_getattr(self):
        x = self.x
        x.ca.a = 2
        self.assertEqual(x.ca.a, 2)
        self.assertEqual(x.ca.b, 12.5)
        self.assertIs(x.ca.c, None)

    def test_ComposedAtt_is_unsettable(self):
        with self.assertRaises(AttributeError):
            self.x.ca = 2
        
    def test_ComposedAtt_does_not_accept_required_att(self):
        with self.assertRaises(AttributeError):
           class Y:
                ca = ComposedAtt(
                    a = (int, Att.required),
                    b = 1.2,
                )

class ComposedAtt_inClassTest(ComposedAttTest):
    def setUp(self):            
        class X(metaclass=Class):
            ca = ComposedAtt(
                a = Att(int),
                b = (float, 12.5),
                c = str,
            )
            i = int
            f = float, 1.2
        self.x = X()
    def test_basic_getattr(self):
        super().test_basic_getattr()
        x = self.x
        self.assertEqual(x.f, 1.2)
        self.assertIs(x.i, None)

class ClassWithSimplifyAttrNotation(unittest.TestCase):
    def setUp(self):
        E = Enum('E', "a b c")
        class X(metaclass=Class):
            i = int
            f = float, 1.2
            s = str
            x = Att()
            e = E, E.a
            dt = datetime(2018, 8, 7)
            def m(self): pass
        self.E = E
        self.X = X

##class ClassWithSimplifyAttrNotation(unittest.TestCase):
##    def setUp(self):
##        class X(metaclass=Class):
##            ii = int, 12, Att.required
##            ss = Att.required, "example", str
##            # et si pas de valeur par défaut?
##            i = 1
##            s = str
##            f = float, 1.2
##            L = [1,2]
##        self.X = X
##    def test_get_att_default_value(self):
##        x = self.X()
##        self.assertEqual(x.i, 1)
##        self.assertEqual(x.f, 1.2)
##        self.assertEqual(x.ii, 12)
##        self.assertIs(x.s, None)
##        self.assertEqual(x.ss, "example")
##        self.assertListEqual(x.L, [1,2])
##    def test_set_att(self):
##        x = self.X()
##        x.i = 12
##        self.assertEqual(x.i,12)
##        x.s = "s"
##        self.assertEqual(x.s, "s")
##        x.f = 12.1
##        self.assertEqual(x.f, 12.1)
##        x.ii = 13
##        self.assertEqual(x.ii, 13)
##        x.ss = "ss"
##        self.assertEqual(x.ss, "ss")
##        x.L.append(3)
##        self.assertListEqual(x.L, [1,2,3])
##    def test_set_att_to_none(self):
##        x = self.X()
##        x.i = None
##        self.assertIs(x.i,None)
##        x.f = None
##        self.assertIs(x.f,None)
##        x.s = None
##        self.assertIs(x.s,None)
##        x.ii = None
##        self.assertIs(x.ii,None)
##        x.ss = None
##        self.assertIs(x.ss,None)
##    def test_set_att_with_catch_typed_value(self):
##        x = self.X()
##        x.i = "12"
##        self.assertEqual(x.i, 12)
##        x.f = "12"
##        self.assertEqual(x.f, 12.0)
##        x.s = 12
##        self.assertEqual(x.s, "12")
##        x.ss = 12
##        self.assertEqual(x.ss, "12")
##        x.ii = "12"
##        self.assertEqual(x.ii, 12)
##    def test_att_type(self):
##        self.assertIs(self.X.i.type, int)
##        self.assertIs(self.X.f.type, float)
##        self.assertIs(self.X.s.type, str)
##        self.assertIs(self.X.ii.type, int)
##        self.assertIs(self.X.ss.type, str)
##        self.assertIs(self.X.L.type, list)
##        x = self.X()
##        self.assertIs(type(x.i), int)
##        self.assertIs(type(x.f), float)
##        self.assertIs(type(x.s), type(None))
##        self.assertIs(type(x.ii), int)
##        self.assertIs(type(x.ss), str)
##        self.assertIs(type(x.L), list)
##    def test_init_method(self):
##        x = self.X(13, "ss", 12, s="test", f=5.3, L=['A','B'])
##        self.assertEqual(x.i, 12)
##        self.assertEqual(x.f, 5.3)
##        self.assertEqual(x.s, "test")
##        self.assertEqual(x.ii, 13)
##        self.assertEqual(x.ss, "ss")
##        self.assertListEqual(x.L, ['A','B'])
##    def test_att_str_default_empty(self):
##        class Y(metaclass=Class):
##            SSS = ""
##        y = Y()
##        self.assertIs(Y.SSS.type, str)
##        self.assertIs(type(y.SSS), str)
##        self.assertEqual(y.SSS, "")
                 
class ClassOfClassTest(unittest.TestCase):
    def setUp(self):
        class YT(Class, metaclass=Class):
            n = str
            
        class Y(metaclass=YT): pass
        class X(metaclass=YT): 
            N = int
        self.YT = YT; self.Y = Y; self.X = X

    def test_set(self):
        self.Y.n = "Y"; self.X.n = "X"
        self.assertEqual(self.Y.n, "Y")
        self.assertEqual(self.X.n, "X")

    def test_link_between_classes_of_class(self):
        class XT(Class, metaclass=Class): pass
        class R(metaclass=Relation):
            __cinit__ = self.YT
            __cfin__ = XT
        R2 = Link(self.YT, "R2", XT)

    def test_hierarchy(self):
        class XT(self.YT, metaclass=Class):
            i = int
        class X(metaclass=XT): pass
        X.n = "xxx"
        X.i = 2
        
                
class RelationTest(unittest.TestCase):

    def setUp(self):
        # these 3 classes represent 3 types of classes which can be linked
        class X(object):
            A = 1        
        class Y:
            pass            
        class Z(metaclass=Class):
            i = Att(int)
            f = Att(float, 1.2)
        
        class RXY(object, metaclass=Relation):
            __cinit__ = X
            __cfin__ = Y
        class RXX(object, metaclass=Relation):
            __cinit__ = X
            __cfin__ = X

        class RYZ(object, metaclass=Relation):
            __cinit__ = Y
            __cfin__ = Z
            
        self.X = X; self.Y = Y; self.Z = Z
        self.RXY = RXY
        self.RXX = RXX
        self.RYZ = RYZ
        
    def test_relations_between_classes(self):
        self.assertIs(type(self.RXY), Relation)
        # PB utilisation d'attribut qui n'existent pas au niveau utilisateur
        self.assertIs( self.RXY.__cinit__, self.X )
        self.assertIs( self.RXY.__cfin__, self.Y )
        self.assertIs( self.RXX.__cinit__, self.X )
        self.assertIs( self.RXX.__cfin__, self.X )
        self.assertIs( self.RYZ.__cinit__, self.Y )
        self.assertIs( self.RYZ.__cfin__, self.Z )
        self.assertEqual(len(self.X.__psc__), 2)
        self.assertEqual(len(self.X.__nsc__), 1)
        self.assertEqual(len(self.Y.__psc__), 1)
        self.assertEqual(len(self.Y.__nsc__), 1)
        self.assertEqual(len(self.Z.__psc__), 0)
        self.assertEqual(len(self.Z.__nsc__), 1)
        self.assertIs( self.X.__psc__[0], self.RXY )
        self.assertIs( self.Y.__nsc__[0], self.RXY )
        self.assertIs( self.X.__psc__[1], self.RXX )
        self.assertIs( self.X.__nsc__[0], self.RXX )
        self.assertIs( self.Y.__psc__[0], self.RYZ )
        self.assertIs( self.Z.__nsc__[0], self.RYZ )

    def test_instances_of_2_linked_classes(self):
        x = self.X(); y = self.Y()
        self.assertEqual(len(x.__psc__), 0)
        self.assertEqual(len(x.__nsc__), 0)
        self.assertEqual(len(y.__psc__), 0)
        self.assertEqual(len(y.__nsc__), 0)

    def test_instanciated_relations(self):
        x1 = self.X(); x2 = self.X()
        r = self.RXX(x1, x2)
        self.assertIs(r.__oinit__, x1)
        self.assertIs(r.__ofin__, x2)
        self.assertEqual(len(x1.__psc__), 1)
        self.assertIs(x1.__psc__[0], r)
        self.assertEqual(len(x1.__nsc__), 0)
        self.assertEqual(len(x2.__psc__), 0)
        self.assertEqual(len(x2.__nsc__), 1)
        self.assertIs(x2.__nsc__[0], r)
        
    def test_cut_relations(self):
        x1 = self.X(); x2 = self.X()
        y = self.Y()            
        rx1x2 = self.RXX(x1, x2)
        rx1y = self.RXY(x1, y)
        rx2y = self.RXY(x2, y)
        self.assertEqual(len(x1.__psc__), 2)
        self.assertIs(x1.__psc__[0], rx1x2)
        self.assertIs(x1.__psc__[1], rx1y)
        self.assertEqual(len(x1.__nsc__), 0)

        self.assertEqual(len(x2.__psc__), 1)
        self.assertIs(x2.__psc__[0], rx2y)
        self.assertEqual(len(x2.__nsc__), 1)
        self.assertIs(x2.__nsc__[0], rx1x2)

        self.assertEqual(len(y.__psc__), 0)
        self.assertEqual(len(y.__nsc__), 2)
        self.assertIs(y.__nsc__[0], rx1y)
        self.assertIs(y.__nsc__[1], rx2y)

        rx1x2.cut()
        self.assertEqual(len(x1.__psc__), 1)
        self.assertIs(x1.__psc__[0], rx1y)
        self.assertEqual(len(x1.__nsc__), 0)

        self.assertEqual(len(x2.__psc__), 1)
        self.assertIs(x2.__psc__[0], rx2y)
        self.assertEqual(len(x2.__nsc__), 0)

        self.assertEqual(len(y.__psc__), 0)
        self.assertEqual(len(y.__nsc__), 2)
        self.assertIs(y.__nsc__[0], rx1y)
        self.assertIs(y.__nsc__[1], rx2y)

        rx1y.cut()
        self.assertEqual(len(x1.__psc__), 0)
        self.assertEqual(len(x1.__nsc__), 0)

        self.assertEqual(len(x2.__psc__), 1)
        self.assertIs(x2.__psc__[0], rx2y)
        self.assertEqual(len(x2.__nsc__), 0)

        self.assertEqual(len(y.__psc__), 0)
        self.assertEqual(len(y.__nsc__), 1)
        self.assertIs(y.__nsc__[0], rx2y)

    def test_set__psc____nsc__(self):
##        with self.assertRaises(AttributeError):
##            self.X.__psc__ = 12
##        with self.assertRaises(AttributeError):
##            self.X.__nsc__ = 12
        x1 = self.X()
        with self.assertRaises(AttributeError):
            x1.__psc__ = "a"
        with self.assertRaises(AttributeError):
            x1.__nsc__ = "a"

class ReInitRelationTest(RelationTest):
    def setUp(self):
        class X(object):
            A = 1        
        class Y:
            pass            
        class Z(metaclass=Class):
            i = Att(int)
            f = Att(float, 1.2)
        
        class RXY(object, metaclass=Relation):
            __cinit__ = X
            __cfin__ = Y
        class RXX(object, metaclass=Relation):
            __cinit__ = X
            __cfin__ = X
            j = Att(int)
            s = Att(str, "xx")
        class RYZ(object, metaclass=Relation):
            __cinit__ = Y
            __cfin__ = Z
            j = Att(int)
            s = Att(str, "xx")
        self.X = X; self.Y = Y; self.Z = Z
        self.RXY = RXY
        self.RXX = RXX
        self.RYZ = RYZ

    def test_init_values(self):
        x = self.X(); y = self.Y(); z = self.Z(1)
        rxy = self.RXY(x, y)
        rxx = self.RXX(x, x, 1)
        self.assertEqual(rxx.j, 1)
        self.assertEqual(rxx.s, "xx")
        ryz = self.RYZ(y, z, 1, "a")
        self.assertEqual(ryz.j, 1)
        self.assertEqual(ryz.s, "a")
        
        
class RelationErrorsTest(unittest.TestCase):
    pass
    
class RelationWithClassAttrTest(unittest.TestCase):

    def test_Fonctor_with_hbds(self):
        class X(metaclass=Class):
            a = Att(int)
            b = Att(float)
            c = Att(str, "sss")
            d = Att(bool, True)
        r = set(('a', 'b', 'c', 'd'))
        self.assertSetEqual(set([a.name for a in X | ATT]), r) 
        self.assertSetEqual(set([a.name for a in X() | CLASS | ATT]), r) 

        self.assertSetEqual( X() | OATT, set((None, 'sss', True)))
        self.assertSetEqual(X() | OATT | CLASS, set((type(None), str, bool)))
        
class FonctorRelationTest(unittest.TestCase):
    def setUp(self):
        class XC(metaclass=Class):
            pass
        class YC(metaclass=Class):
            pass
        class ZC(metaclass=Class):
            pass
        class RXY(metaclass=Relation):
            __cinit__ = XC
            __cfin__ = YC
        class RXZ(metaclass=Relation):
            __cinit__ = XC
            __cfin__ = ZC
        self.XC = XC; self.YC = YC; self.ZC = ZC
        self.RXY = RXY; self.RXZ = RXZ
        
    def test__psc__(self):
        self.assertSetEqual(self.XC | PSC, set((self.RXY, self.RXZ)))

    def test__nsc__(self):
        self.assertSetEqual( self.XC | NSC, set())
        self.assertSetEqual(self.YC | NSC, set((self.RXY,)))

    def test_init(self):
        self.assertSetEqual( self.RXY | INIT, set((self.XC,)))
        
    def test_fin(self):
        self.assertSetEqual((self.RXY, self.RXZ) | FIN, set((self.YC, self.ZC)))

    def test_opsc_ofin(self):
        x = self.XC(); y = self.YC()
        self.RXY(x, y)
        self.assertSetEqual(x | OPSC | OFIN, set((y,)))
        z = self.ZC()
        self.RXZ(x, z)
        self.assertSetEqual(x | OPSC | OFIN, set((y, z)))
        self.assertSetEqual(x | OPSCR(self.RXZ) | OFIN, set((z,)))
    
    def test_onsc_ofin(self):
        x = self.XC(); y = self.YC()
        self.RXY(x, y)
        self.assertSetEqual(y | ONSC | OINIT, set((x,)))
        z = self.ZC()
        self.RXZ(x, z)
        self.assertSetEqual((y, z) | ONSC | OINIT, set((x,)))
        self.assertSetEqual((y, z) | ONSCR(self.RXY) | OINIT, set((x,)))

class CreateRelationTest(FonctorRelationTest):
    def setUp(self):
        class XC(metaclass=Class):
            pass
        class YC(metaclass=Class):
            pass
        class ZC(metaclass=Class):
            pass
        self.XC = XC; self.YC = YC; self.ZC = ZC
        self.RXY = create_relation(XC, 'RXY', YC)
        self.RXZ = create_relation(XC, 'RXZ', ZC)

class ClassRoleTest(unittest.TestCase):
    def setUp(self):
        class XC(metaclass=Class):
            y = Role('RXY')
        class YC(metaclass=Class):
            pass
        class ZC(metaclass=Class):
            pass
        self.XC = XC; self.YC = YC; self.ZC = ZC
        self.RXY = create_relation(XC, 'RXY', YC)
        self.RXZ = create_relation(XC, 'RXZ', ZC)

    def test_role(self):
        x = self.XC(); y1 = self.YC; y2 = self.YC()
        self.RXY(x, y1)
        self.RXY(x, y2)
        self.assertEqual(len(x.y), 2)
        xp1, xp2 = x.y
        self.assertTrue(y1 in x.y)
        self.assertTrue(y2 in x.y)

    def test_role_in_class_of_class(self):
        class Pawn(Class, metaclass=Class):
            id = int
            equipments = Role("R_Pawn_Equipment")
        class EquipmentType(Class, metaclass=Class):
            id = int
        R_Pawn_Equipment = Link(Pawn, "R_Pawn_Equipment", EquipmentType)

        class P(metaclass=Pawn): pass
        P.id = 1
        self.assertSetEqual(P.equipments, set())

def load_tests(loader, standard_tests, pattern):
    # add new doctest tests
    import doctest
    from ADT import hbds
    standard_tests.addTests(doctest.DocTestSuite(hbds))
    return standard_tests

if __name__ == '__main__':
    unittest.main(
##        defaultTest=(
####        'ClassRoleTest.test_role_in_class_of_class',
##            'CreateAttTest',
##            )
        )
    
