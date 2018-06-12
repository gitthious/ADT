# -*- coding: utf-8 -*-
"""
The aim of this package is to provide Generic Abrastact Data Type (ADT) used to
describe Data Structure in Pythonic fashon.

If you want to describe en USAdress data type, you can write:
class USAddress:
    state = ""
    city = ""
    street = ""
    zipcode = None
    country = ""

This class is available in Python but you don't describe like this all structure
contol you need, like it's possible for instance in xsd (XML Scheme).
Thurethemore, when you create a instance you can write:

u = USAdress() # and you instanciate it with any control.

You can write again:

u.city = 12
USAdress.other = 13
USAdress.city = 3; u = USAdress()
>>> print u.city
>>> 3

It's a nosense regards the definition you wanted first

ADT module permite you to create USADRESS strong definition:

import ADT
class USAddress:
    __metaclass__ = Class
    state = Attr(str)
    city = Attr(str)
    street = Attr(str)
    zipcode = Attr(int,12)
    country = Attr(str)

All you can do in Python are available except that we come to see "plus haut".
And all type controls are doing and raise a exception if not expected.

>>> u.city = 12
>>> raise TypeError: Bad type int of value 12 for Att 'city'. Expected type is 'str'

TODO:
    docstring automatique

Les attributs sont dérivés des properties python
    en passant un type, mais supportent l'absence de type comme en python

Ajouter les attribut composés
    X.attcom.att

Ajouter les relations entre classes
    se sont des collections
    
"""
import collections, sys, inspect, types
from .fonctors import getattrsfromdict, getattrs, Fonctor, IDENT, to_iterable, OATT


class Class(type):    

    def __new__(cls, clsname, bases, clsdict):
##        print('Class.__new__', clsdict)
        cls.make_attributes(clsname, clsdict)
        cls.make_init_method(clsdict)
        clsobj = type.__new__(cls, clsname, bases, clsdict)
        return clsobj

    @classmethod
    def make_attributes(cls, clsname, clsdict):
        for att in getattrsfromdict(clsdict):
            val = clsdict[att]
            # to detect embeded class definitions as
            # class C(metaclass=Class):
            #   class X(metaclass=Class):  et class X tout cours?
            if inspect.isclass(val) and isinstance(val, Class): continue
            if not isinstance(val, tuple): val = (val,)
            clsdict[att] = Class.make_simplified_attribute(att, *val)
            
    @classmethod
    def make_simplified_attribute(cls, att, *vals):
        """
        Return an *Att* instance from tuple *vals*.
        The tuple is interpreted as:
         * (object)
         * (class)
         * (class, Att.required)
         * (object, Att.required)
         * (class, object)
         * (class, default object, Att.required)
        representing all possible combinations of Att parameters
        Otherwise, **AttributeError** is raised.
        """
        err = "'%s' attribute declaration doesn't repect Att constructor" % att
        typ, default, mandatory = None, None, False
        if len(vals) < 1 or len(vals) > 3:
            raise AttributeError(err)
        # because order is not important, so re-order vals
        for v in vals:
            if v is Att.required: mandatory = True
            elif inspect.isclass(v): typ = v
            else: default = v
        if isinstance(default, Att):
            if len(vals) != 1: raise AttributeError(err)
            return default
        elif isinstance(default, ComposedAtt):
            return default
        if default and not typ:
            typ = type(default)
        return Att(typ, default, mandatory)

    @classmethod
    def make_init_method(cls, clsdict):
        code_body, code_args = cls.make_code_args(clsdict)
        if len(code_args) == 0: return
        code = 'def __init__(self, %s):\n' % ', '.join(code_args)
        code += code_body
##        print(code)
        try:
            exec(code , globals(), clsdict)
        except:
            print(code)
            raise
        

    @classmethod
    def make_code_args(cls, clsdict):
        attrs = [a for a in clsdict if isinstance(clsdict[a], Att)]
        code_args = []
        code_body = ""
        for attr in attrs:
            att = clsdict[attr]
            if att.default is not None:
                code = "%s=%s.default" % (attr, attr)
            else:
                if att.mandatory:
                    code = "%s" %(attr)
                else:
                    code = "%s=None" % (attr)            
            code_args.append(code)
            code_body += '    self.%s = %s\n' % (attr, attr)
        return code_body, code_args

def create_class(name, attr_defs):
    """
    Return class from *name* and *attr_defs* dictinary.
    Do the same thing as instruction:
    class X(metaclass=Class):
        a1 = Att(int, 1)
        a2 = float
    with *name* = 'X' and *attr_defs* = {'a1': Att(int, 1), 'a2': Att(float)}
    see Class and Att definitions.
    """
    meta = {'metaclass': Class }
    def update(clsdic):
        for att, val in attr_defs.items():
            clsdic[att] = val
    return types.new_class(name, kwds=meta, exec_body=update)

def strict(cls):
    """
    Decorator for Class to avoid usage of undeclared attribute.
    Raise AttributeError exception if attribute is used but not declare.
    @strict
    > class X(metaclass=Class):
        i = Att(int)
    > x = X()
    > x.i =1
    > x.j =2 => raise AttributeError
    """
    def attrset(self, attr, val):
        if not hasattr(self, attr):
            raise AttributeError("Class '%s' doesn't declare attribute '%s'" \
                                 % (cls.__name__, attr))
        super(cls, self).__setattr__(attr, val)
    cls.__setattr__ = attrset
    return cls

class Att:
    class required: pass
    def __init__(self, att_type=None, default=None, mandatory=False,
                 doc=None, constraint=None):
        # tester si self.type is None and owner class is hbds.Class
        self.type = att_type
        self.mandatory = mandatory
        self.doc = doc
        self.constraint = constraint
        self.name = None
        self.default = self.validate(default)
            
    def __get__(self, instance, owner):
##        print('Att.__get__', instance, owner)
        if instance is None:
            # return class attribute itself
            return self 
        return instance.__dict__.get(self.name, self.default)
        
    def validate(self, value):
        if value is None: return value
        # try to catch value with type
        if self.type:
##            if self.type is ComposedAtt:
##                return value
            if not isinstance(value, self.type):
                try:
                    value = self.type(value)
                except ValueError:
                    raise ValueError(
                              "Bad type '%s' of value '%s' for Att '%s'. " %
                              (str(type(value)), str(value), self.name)
                            + "Expected type is '%s' or accepted others values" % str(self.type)
                    )
        # try apply contraint
        if self.constraint:
            self.constraint(value)
        return value
    def __set__(self, instance, value):
##        print('Att.__set__', instance, value)
        instance.__dict__[self.name] = self.validate(value)
    def __set_name__(self, cls, name):
        self.name = name
    def __repr__(self):
        s = "%s = Att(type=%s, default=%s, mandatory=%s)"
        return s % (self.name, self.type, self.default, self.mandatory)

class ComposedAtt:
    
    def __init__(self, **attr_defs):
        name = "%s_tmp" % self.__class__.__name__
        self._class = create_class(name, attr_defs)
        L = [v for v in self._class | OATT \
               if isinstance(v, Att) and v.mandatory and not v.default]
        if len(L) != 0:
            raise AttributeError("Impossible to use mandatory attribute without default value in ComposedAtt")

    def __get__(self, instance, ownerclass):
##        print('ComposedAtt.get', instance, ownerclass)
        if not instance: return self._class()
        return instance.__dict__.setdefault(self._name, self._class())

    def __set__(self, instance, value):
        raise AttributeError("%s '%s' of %s is'nt settable" % \
                    (type(self).__name__, self._name, instance))

    def __set_name__(self, cls, name):
        self._name = name
        self._class.__name__ = "%s_%s" % (self.__class__.__name__, name)

"""
Cardinalités des rôles des relations

L: X (n,m) -> (n,m) Y

@noreverse
    pour ne pas implémenter le negative semi cocircuit
    nommer la relation inverse => inverser les psc, nsp

Optimisation de l'acces
    if m == 1:  SC != list

Contrôles relatifs aux cardinalités
    if m is not None: n <= m
    if m is not None: contrôle si len(sc) == m avant création de la relation
    if n != 0:
        => contraintes à la création des objets init et fin
        si ni != 0 => nf == 0 et inversement
        X (2, 3) (0,2) Y
            X(..., y1, y2)
        X(0,2) (1,3) Y
            Y(..., x1)
    m = 'all' => relation avec tous les Y?

"""

class SemiCocircuit:
    attrs = ("__psc__", "__nsc__")
    def __init__(self):
        self.sc = []
    def __get__(self, obj, cls):
        try:
            # this occur really often, for object instance
            return obj.__dict__[self.attr].sc
        except KeyError:
            # this occur one time of object if attr not in obj.__dict__
            create_semi_cocircuit(self.attr, obj)
            return obj.__dict__[self.attr].sc
        except AttributeError:
            # this occur if obj is None, when uses class attribute
            return self.sc
    def __set__(self, obj, value):
        raise AttributeError(str(self.attrs) + " are not settable")

class PositiveSemiCocircuit(SemiCocircuit):
    attr = "__psc__"

class NegativeSemiCocircuit(SemiCocircuit):
    attr = "__nsc__"

table = {
    "__nsc__" : NegativeSemiCocircuit,
    "__psc__" : PositiveSemiCocircuit,
    }
def create_semi_cocircuit(attr, obj):
    if attr in obj.__dict__: return
    obj.__dict__[attr] = table[attr]()

class Relation(Class):

    def __new__(cls, clsname, bases, clsdict):
        if '__cinit__' not in clsdict:
            raise AttributeError("Relation must define the '__cinit__' class")
        if '__cfin__' not in clsdict:
            raise AttributeError("Relation must define the '__cfin__' class")
        if '__cards__' not in clsdict:
            # set default cardinalities
            clsdict['__cards__'] = ((0,'m'),(0,'m'))
        clsobj = Class.__new__(cls, clsname, bases, clsdict)
        return clsobj

    @classmethod
    def make_init_method(cls, clsdict):
        code_body, code_args = cls.make_code_args(clsdict)
        code = 'def __init__(self, oinit, ofin, %s):\n' % ', '.join(code_args)
        code_body += "    self.__oinit__ = oinit\n"
        code_body += "    self.__ofin__ = ofin\n"
        code_body += "    self.__oinit__.__psc__.append(self)\n"
        code_body += "    self.__ofin__.__nsc__.append(self)\n"
        code += code_body
        exec(code , globals(), clsdict)

    def __init__(rel, name, bases, clsdict):
        super(Relation, rel).__init__(name, bases, clsdict)
        assert rel.__cinit__ and rel.__cfin__
        def init_sc(cls):
            if not hasattr(cls, "__psc__"):
                setattr(cls, "__psc__", PositiveSemiCocircuit())
            if not hasattr(cls, "__nsc__"):
                setattr(cls, "__nsc__", NegativeSemiCocircuit())
        init_sc(rel.__cinit__)
        rel.__cinit__.__psc__.append(rel)
        init_sc(rel.__cfin__)
        rel.__cfin__.__nsc__.append(rel)
       
        def cut(self):
            self.__oinit__.__psc__.remove(self)
            self.__ofin__.__nsc__.remove(self)
        rel.cut = cut

def create_relation(cinit, name, cfin):
    meta = {'metaclass': Relation, }
    def update(clsdic):
        clsdic['__cinit__'] = cinit
        clsdic['__cfin__'] = cfin
    return types.new_class(name, kwds=meta, exec_body=update)
# Alias
Link = create_relation


PSC = Fonctor(lambda cls: cls.__psc__)
NSC = Fonctor(lambda cls: cls.__nsc__)

INIT = Fonctor(lambda rel: rel.__cinit__)
FIN = Fonctor(lambda rel: rel.__cfin__)

def opsc(obj, rel=None):
    if rel is None: return obj.__psc__
    return [r for r in obj.__psc__ if isinstance(r, rel)]
OPSC = Fonctor(opsc)
OPSCR = Fonctor(opsc)

def onsc(obj, rel=None):
    if rel is None: return obj.__nsc__
    return [r for r in obj.__nsc__ if isinstance(r, rel)]
ONSC = Fonctor(onsc)
ONSCR = Fonctor(onsc)


OINIT = Fonctor(lambda r: r.__oinit__)
OFIN = Fonctor(lambda r: r.__ofin__)

# définir aussi le foncteur OBJ

class Role:
# Role doit dériver de Att
# Faire un role qui retourne un objet et non une liste (fct de la card de R?)
    def __init__(self, relname):
        self.relname = relname
    def __get__(self, instance, owner_cls):
        rel = [r for r in owner_cls | PSC if r.__name__ == self.relname][0]
        # et si rel is None?
        return instance | OPSCR(rel) | OFIN


# Faire des relations ordered...et les foncteurs qui vont avec
# Optimiser les foncteurs pour éviter de tous parcourir si pas nécessaire

if __name__ == '__main__':
    class X: pass
    class Y: pass
    class R(metaclass=Relation):
        __cinit__ = X
        __cfin__ = Y

