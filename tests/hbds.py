# -*- coding: utf-8 -*-

import unittest
from ADT.basictypes import enum, date
from ADT.fonctors import CLASS, ATT, OATT
from fonctors import expected_fonctor
from ADT.hbds import *

# tester Att

class ClassAndAttrTest(unittest.TestCase):
    def setUp(self):
        E = enum.Enum('E', "a b c")
        class X(metaclass=Class):
            i = Att(int)
            f = Att(float, 1.2)
            s = Att(str)
            x = Att()
            e = Att(E, E.a) 
            def m(self): pass
        self.E = E
        self.X = X

    def test_getattrs_class(self):
        attrs = getattrs(self.X)
        self.assertEqual( len(attrs), 5)
        for attr in attrs:
            self.assertIn( attr, ["i", "f", "s", "x", "e"])

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
        with self.assertRaises(ValueError):
            x.i = "aa"

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
        with self.assertRaises(ValueError):
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
        

class ScrictClassAndAttrTest(ClassAndAttrTest):
    def setUp(self):
        E = enum.Enum('E', "a b c")
        @strict
        class X(metaclass=Class):
            i = Att(int)
            f = Att(float, 1.2)
            s = Att(str)
            x = Att()
            e = Att(E, E.a)
            def m(self): pass
        self.X = X
        self.E = E
    def test_set_undeclared_att(self):
        x = self.X()
        with self.assertRaises(AttributeError):
            x.z = 12
                                 

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
        class X(metaclass=Class):
            ii = int, 12, Att.required
            ss = Att.required, "example", str
            # et si pas de valeur par défaut?
            i = 1
            s = str
            f = float, 1.2
            L = [1,2]
        self.X = X
    def test_get_att_default_value(self):
        x = self.X()
        self.assertEqual(x.i, 1)
        self.assertEqual(x.f, 1.2)
        self.assertEqual(x.ii, 12)
        self.assertIs(x.s, None)
        self.assertEqual(x.ss, "example")
        self.assertListEqual(x.L, [1,2])
    def test_set_att(self):
        x = self.X()
        x.i = 12
        self.assertEqual(x.i,12)
        x.s = "s"
        self.assertEqual(x.s, "s")
        x.f = 12.1
        self.assertEqual(x.f, 12.1)
        x.ii = 13
        self.assertEqual(x.ii, 13)
        x.ss = "ss"
        self.assertEqual(x.ss, "ss")
        x.L.append(3)
        self.assertListEqual(x.L, [1,2,3])
    def test_set_att_to_none(self):
        x = self.X()
        x.i = None
        self.assertIs(x.i,None)
        x.f = None
        self.assertIs(x.f,None)
        x.s = None
        self.assertIs(x.s,None)
        x.ii = None
        self.assertIs(x.ii,None)
        x.ss = None
        self.assertIs(x.ss,None)
    def test_set_att_vith_catch_typed_value(self):
        x = self.X()
        x.i = "12"
        self.assertEqual(x.i, 12)
        x.f = "12"
        self.assertEqual(x.f, 12.0)
        x.s = 12
        self.assertEqual(x.s, "12")
        x.ss = 12
        self.assertEqual(x.ss, "12")
        x.ii = "12"
        self.assertEqual(x.ii, 12)
    def test_att_type(self):
        self.assertIs(self.X.i.type, int)
        self.assertIs(self.X.f.type, float)
        self.assertIs(self.X.s.type, str)
        self.assertIs(self.X.ii.type, int)
        self.assertIs(self.X.ss.type, str)
        self.assertIs(self.X.L.type, list)
        x = self.X()
        self.assertIs(type(x.i), int)
        self.assertIs(type(x.f), float)
        self.assertIs(type(x.s), type(None))
        self.assertIs(type(x.ii), int)
        self.assertIs(type(x.ss), str)
        self.assertIs(type(x.L), list)
    def test_init_method(self):
        x = self.X(13, "ss", 12, s="test", f=5.3, L=['A','B'])
        self.assertEqual(x.i, 12)
        self.assertEqual(x.f, 5.3)
        self.assertEqual(x.s, "test")
        self.assertEqual(x.ii, 13)
        self.assertEqual(x.ss, "ss")
        self.assertListEqual(x.L, ['A','B'])
    def test_att_str_default_empty(self):
        class Y(metaclass=Class):
            SSS = ""
        y = Y()
        self.assertIs(Y.SSS.type, None)
        self.assertIs(type(y.SSS), str)
        self.assertEqual(y.SSS, "")
        

            
##    class ClassWithUserDefinedAttTypeTest(unittest.TestCase):
##            
##        def test_PositiveInt(self):
##            class X():
##                __metaclass__ = Class
##                a = PositiveInteger(mandatory=True)
##                b = PositiveInt(2)
##                c = PositiveInt()
##            x = X(1)
##            self.assertEqual(x.a, 1)
##            self.assertEqual(x.b, 2)
##            self.assertIsNone(x.c)
##            x.c = 3
##            self.assertEqual(x.c, 3)
##            with self.assertRaises(ValueError):
##                x.a = -2
##            with self.assertRaises(ValueError):
##                class Y():
##                    __metaclass__ = Class
##                    a = PositiveInt(-2)
         
        
        
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
        f = X | ATT
        r = ('a', 'b', 'c', 'd')
        expected_fonctor(self, f, r)
        f = X() | CLASS | ATT 
        expected_fonctor(self, f, r)

        f = X() | OATT 
        r = (None, 'sss', True)
        expected_fonctor(self, f, r)
        f = X() | OATT | CLASS
        r = (type(None), str, bool)
        expected_fonctor(self, f, r)
        
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
        f = self.XC | PSC
        r = (self.RXY, self.RXZ)
        expected_fonctor(self, f, r)

    def test__nsc__(self):
        f = self.XC | NSC
        r = []
        expected_fonctor(self, f, r)
        f = self.YC | NSC
        r = (self.RXY,)
        expected_fonctor(self, f, r)

    def test_init(self):
        f = self.RXY | INIT
        r = (self.XC,)
        expected_fonctor(self, f, r)
        
    def test_fin(self):
        f = (self.RXY, self.RXZ) | FIN
        r = (self.YC, self.ZC)
        expected_fonctor(self, f, r)

    def test_opsc_ofin(self):
        x = self.XC(); y = self.YC()
        self.RXY(x, y)
        f = x | OPSC | OFIN
        r = (y,)
        expected_fonctor(self, f, r)
        z = self.ZC()
        self.RXZ(x, z)
        f = x | OPSC | OFIN
        r = (y, z)
        expected_fonctor(self, f, r)
        f = x | OPSCR(self.RXZ) | OFIN
        r = (z,)
        expected_fonctor(self, f, r)
    
    def test_onsc_ofin(self):
        x = self.XC(); y = self.YC()
        self.RXY(x, y)
        f = y | ONSC | OINIT
        r = (x,)
        expected_fonctor(self, f, r)
        z = self.ZC()
        self.RXZ(x, z)
        f = (y, z) | ONSC | OINIT
        r = (x,)
        expected_fonctor(self, f, r)
        f = (y, z) | ONSCR(self.RXY) | OINIT
        r = (x,)
        expected_fonctor(self, f, r)

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

if __name__ == '__main__':
    unittest.main() 
##    unittest.main(defaultTest=(
##        'ComposedAttTest.test_ComposedAtt_does_not_accept_required_att',
##    'ClassWithSimplifyAttrNotation',
##        ) ) 
