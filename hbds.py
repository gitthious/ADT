# -*- coding: utf-8 -*-
"""
The aim of this module is to provide Generic Abrastact Data Type (ADT) used to
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
print u.city
3

It's a nosense regards the definition you wanted first

ADT module permite you to create USADRESS strong definition:

import ADT
class USAddress(metaclass=Class):
    state = Attr(str)
    city = Attr(str)
    street = Attr(str)
    zipcode = Attr(int,12)
    country = Attr(str)

All you can do in Python are available except that we come to see above.
And all type controls are doing and raise a exception if not expected.

u.city = 12
raise TypeError: Bad type int of value 12 for Att 'city'. Expected type is 'str'

TODO:
    docstring __init__ automatiques
    docstring des atts
    raise explicite dans l'init généré des classes

Références:
 * HBDS: http://pelle.stephane.free.fr/HBDSConseils.htm
 * https://rhettinger.wordpress.com/2011/05/26/super-considered-super/
 * https://blog.ionelmc.ro/2015/02/09/understanding-python-metaclasses/
 * https://docs.python.org/3.6/howto/descriptor.html
 * module attrs (http://www.attrs.org/en/stable/)
 * module leaflet
 * module dataclasses (https://docs.python.org/3/library/dataclasses.html)
"""

import collections, sys, inspect, types, enum
from .fonctors import getattrsfromdict, getattrs, Fonctor, IDENT, to_iterable
from .units import Unit

class Att:
    """
    Used to define a class attribute and then to get, if needed:
     * existing control
     * type control
     * default value
     * and also mandatory information, docstring and contrainst function.
    at intance level.
    Att is a python descriptor, so must be use as class variable
    in class definition.
    """
    
    class required:
        """
        Just to tell if Att is mandarory (or required). See Att.__init__.
        """
        pass

    def __init__(self, att_type=None, default=None, mandatory=False,
                 doc=None, constraint=None, unit=None):
        self.type = att_type
        self.mandatory = mandatory
        self.doc = doc
        self.constraint = constraint
        self.name = None
        self.default = self._validate(default)
        if self.type is None and self.default is not None:
            self.type = type(self.default)
        self.unit = unit
        self.classvars = {}
            
    def __get__(self, instance, ownerclass):
        #print('Att.__get__', self.name, instance, ownerclass)
        if instance is None:
##            return ownerclass.__dict__[self.name]
            for c in ownerclass.__mro__:
                if self.name in c.__dict__:
                    return c.__dict__[self.name]
##            raise AttributeError("type object '%s' and all these mro" 
##                                 "has no attribute '%s'" \
##                                 % (ownerclass.__name__, self.name))
        if isinstance(instance, type):
            return self.classvars[instance]
        return instance.__dict__.get(self.name, self.default)
        
    def _validate(self, value):
        if value is None: return value
        # try to catch value with type
        if self.type:
            if not isinstance(value, self.type):
                try:
                    value = self.type(value)
                except (ValueError, TypeError):
                    m = "'%s' for '%s'. Should be '%s'" % (value, self, self.type)
                    raise TypeError(m)
        # try to apply contraint
        if self.constraint:
            self.constraint(value)
        return value
    
    def __set__(self, instance, value):
        #print('Att.__set__', instance, value)
        value = self._validate(value)
        if isinstance(instance, type):
            self.classvars[instance] = value 
        else:
            instance.__dict__[self.name] = value
        
    def __set_name__(self, cls, name):
##        print("__set_name", cls, name)
        self.name = name
        
    def __repr__(self):
        s = "%s = Att(type=%s, default=%s, mandatory=%s)"
        return s % (self.name, self.type, self.default, self.mandatory)

def create_Att(*vals):
    """
    Return an *Att* instance from tuple *vals*.
    The tuple is interpreted as parameters of Att in any order
    and it may be empty.
    If tuple does'nt respect Att params, **AttributeError** is raised.
    """
    if len(vals) > 4:
        raise TypeError("Too many args for Att (%d). Must be 4 max" % len(vals))

    # because order is not important, so re-order vals
    typ, default, mandatory, unit = None, None, not Att.required, None
    # manque des tests car il peut y avoir 4 valeurs sans Unit par ex.
    for v in vals:
        #print(v)
        if v is Att.required: mandatory = v
        elif isinstance(v, Unit): unit = v
        elif isinstance(v, type): typ = v
        else: default = v
        #print(typ, default, mandatory, unit)

    # vals is already a Att
    if isinstance(default, (Att, ComposedAtt)):
        if len(vals) != 1:
            raise TypeError("Too many Att definition (%d). Use just one" % len(vals))
        return default

    return Att(typ, default, mandatory, unit=unit)


class ComposedAtt:
    
    def __init__(self, **attr_defs):
        name = "%s_tmp" % self.__class__.__name__
        self._class = create_class(name, attr_defs)
        L = [v for v in self._class | ATT if v.mandatory and not v.default]
        if len(L) != 0:
            raise AttributeError("Impossible to use mandatory attribute without default value in ComposedAtt")

    def __get__(self, instance, ownerclass):
        if not instance: return self._class()
        return instance.__dict__.setdefault(self._name, self._class())

    def __set__(self, instance, value):
        raise AttributeError("%s '%s' of %s is'nt settable" % \
                    (type(self).__name__, self._name, instance))

    def __set_name__(self, cls, name):
        self._name = name
        self._class.__name__ = "%s_%s" % (self.__class__.__name__, name)


# Faire une ClassWithInit?: pas sûr que cela soit utile

class Class(type):    
        
    def __new__(cls, clsname, bases, clsdict):
        #print('Class.__new__', cls, clsname, bases, clsdict)
        cls._make_attributes(clsname, clsdict)
        if Class not in [c for b in bases for c in b.__mro__]:
            cls._make_init_method(clsdict)
        
        def fset(instance, att, val):
            #print("%s.__setattr__(fset)" % type(instance).__name__, instance, att, val)
            if not att.startswith('_'):
                if not hasattr(type(instance), att):
                    m = "Class instance '%s' has no Att '%s'"
                    raise AttributeError(m % (instance, att))
            if isinstance(instance, type):
                type.__setattr__(instance, att, val)
            else:
                object.__setattr__(instance, att, val)
        clsdict['__setattr__'] = fset

        clsobj = type.__new__(cls, clsname, bases, clsdict)
        return clsobj        
    
    def __setattr__(cls, att, val):
        #print("Class.__setattr__", cls, att, val)
        if not att.startswith('_'):
            if not hasattr(type(cls), att):
                m = "Class type '%s' has no Att '%s'"
                raise AttributeError(m % (cls, att))
        # super doesn't run here. I don't no why
        #super().__setattr__(att, val)
        type.__setattr__(cls, att, val)
        
    @classmethod
    def _make_attributes(cls, clsname, clsdict):
        
        for att in getattrsfromdict(clsdict):
            val = clsdict[att]

            # to detect embeded class definitions as
            # class C(metclass=Class):
            #   class X(metaclass=Class):  et class X tout cours?
            if inspect.isclass(val) and isinstance(val, Class): continue

            if not isinstance(val, tuple): val = (val,)
            clsdict[att] = create_Att(*val)

            # pas utile à priori
            if not isinstance(clsdict[att], (Att, ComposedAtt)):
                raise TypeError("Attribute must be of type 'Att'")


    @classmethod
    def _make_init_method(cls, clsdict):
        #print('_make_init_method', cls, clsdict)
        code_body, code_args = cls._make_code_args(clsdict)
        if len(code_args) == 0: return
        code = 'def __init__(self, %s):\n' % ', '.join(code_args)
        code += code_body
        #print(code)
        try:
            exec(code , globals(), clsdict)
        except:
            print(code)
            raise
        
    @classmethod
    def _make_code_args(cls, clsdict):
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

def getATT(cls):
    assert isinstance(cls, type)
    A = []
    for a in getattrs(cls):
        v = getattr(cls, a)
        if isinstance(v, Att):
            A.append(v)
    return A
ATT = Fonctor(getATT) 

def getOATT(obj):
    A = []
    for a in getattrs(type(obj)):
        if isinstance(getattr(type(obj), a), Att):
            A.append(getattr(obj,a))
    return A
OATT = Fonctor(getOATT)

def raise_init(cls):
    """
    Decorate the class *cls* to prevent instance creation. It can be use
    for just create simple type that you don't want to instanciate it.
    >>> @raise_init
    ... class Road: pass
    >>> Road()
    Traceback (most recent call last):
    ...
    TypeError: Instance creation is not allowed for <class 'ADT.hbds.Road'>
    """
    def init(self):
        raise TypeError("Instance creation is not allowed for %s" % cls)
    cls.__init__ = init
    return cls


OBJ = Fonctor(lambda cls: getattr(cls, '__obj__'))

def keep_objects_relationship(cls):
    """
    Decorate the class *cls* to add to it a *__obj__* list to keep track
    of all instances of the class.
    You can use it for a class
    >>> @keep_objects_relationship
    ... class X: pass
    >>> x1 = X(); x2 = X()
    >>> X.__obj__ #doctest: +ELLIPSIS
    [<ADT.hbds.X object at 0x...>, <ADT.hbds.X object at 0x...>]
    
    >>> @keep_objects_relationship
    ... class TerrainType(type): pass
    >>> class X(metaclass=TerrainType): pass
    >>> class Y(metaclass=TerrainType): pass
    >>> TerrainType.__obj__ 
    [<class 'ADT.hbds.X'>, <class 'ADT.hbds.Y'>]

    Usage of *__obj__* is just for tests. It's more pretty to use fonctor OBJ
    >>> TerrainType | OBJ
    {<class 'ADT.hbds.X'>, <class 'ADT.hbds.Y'>}

    Warning: decorator must be use only with classes
    with invariant number of instances because __del__ is not implemented!
    """
    if not hasattr(cls, '__obj__'):
        setattr(cls, '__obj__', [])
        
    oldinit = getattr(cls, '__init__', None)
    def newinit(self, *args, **kargs):
        if oldinit:
            oldinit(self, *args, **kargs)
        cls.__obj__.append(self)
    cls.__init__ = newinit

    # Attention: ne fonctionne pas!
##    olddel = getattr(cls, '__del__', None)
##    def newdel(self):
##        if olddel:
##            olddel(sel)
##        cls.__obj__.remove(self)
##    cls.__del__ = newdel
    
    return cls

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

    # Attention:
    #   * pas d'héritage de liens
    #   * et confusion entre SC d'object et SC de type object

    @classmethod
    def create_semi_cocircuit(cls, attr):
        if attr == "__nsc__":
            return NegativeSemiCocircuit()
        return PositiveSemiCocircuit()
        
    def __init__(self):
        self.sc = []
        self.classvars = {}

    def __get__(self, obj, cls):
        if obj is None:
            # when uses class attribute
            return self.sc
        
        if isinstance(obj, type):
            if obj not in self.classvars:
                self.classvars[obj] = self.create_semi_cocircuit(self.attr)
            return self.classvars[obj].sc

        if self.attr not in obj.__dict__:
            obj.__dict__[self.attr] = self.create_semi_cocircuit(self.attr)
        return obj.__dict__[self.attr].sc

    def __set__(self, obj, value):
        raise AttributeError(self.attr + " are not settable")

class PositiveSemiCocircuit(SemiCocircuit):
    attr = "__psc__"

class NegativeSemiCocircuit(SemiCocircuit):
    attr = "__nsc__"


class Relation(Class):

    def __new__(cls, clsname, bases, clsdict):
        if '__cinit__' not in clsdict:
            raise AttributeError("Relation must define the '__cinit__' class")
        if '__cfin__' not in clsdict:
            raise AttributeError("Relation must define the '__cfin__' class")
        if '__cards__' not in clsdict:
            # set default cardinalities
            clsdict['__cards__'] = ((0,'m'),(0,'m'))
        def cut(self):
            self.__oinit__.__psc__.remove(self)
            self.__ofin__.__nsc__.remove(self)
        clsdict['cut'] = cut

        clsobj = Class.__new__(cls, clsname, bases, clsdict)
        return clsobj

    @classmethod
    def _make_init_method(cls, clsdict):
        code_body, code_args = cls._make_code_args(clsdict)
        code = 'def __init__(self, oinit, ofin, %s):\n' % ', '.join(code_args)
        code_body += "    self.__oinit__ = oinit\n"
        code_body += "    self.__ofin__ = ofin\n"
        code_body += "    self.__oinit__.__psc__.append(self)\n"
        code_body += "    self.__ofin__.__nsc__.append(self)\n"
        code += code_body
        try:
            exec(code , globals(), clsdict)
        except:
            print(code)
            raise

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
# les rôles ne sont pas fournit à la complétion
    def __init__(self, relname):
        self.relname = relname
    def __get__(self, instance, owner_cls):
        rel = [r for r in owner_cls | PSC if r.__name__ == self.relname][0]
        # et si rel is None?
        return instance | OPSCR(rel) | OFIN


# Faire des relations ordered...et les foncteurs qui vont avec
# Optimiser les foncteurs pour éviter de tous parcourir si pas nécessaire

class Relation1_to_all(Class):

    def __new__(cls, clsname, bases, clsdict):
        if '__cinit__' not in clsdict:
            raise AttributeError("Relation must define the '__cinit__' class")
        if '__cfin__' not in clsdict:
            raise AttributeError("Relation must define the '__cfin__' class")
        if '__cards__' not in clsdict:
            # set default cardinalities
            clsdict['__cards__'] = ((1,'all'),(None,None))
        def cut(self):
            self.__oinit__.__psc__.remove(self)
        clsdict['cut'] = cut
        
        clsobj = Class.__new__(cls, clsname, bases, clsdict)
        return clsobj

    @classmethod
    def _make_init_method(cls, clsdict):
        code_body, code_args = cls._make_code_args(clsdict)
        code = 'def __init__(self, oinit, ofin, %s):\n' % ', '.join(code_args)
        code_body += "    self.__oinit__ = oinit\n"
        code_body += "    self.__ofin__ = ofin\n"
        code_body += "    self.__oinit__.__psc__.append(self)\n"
        code += code_body
        try:
            exec(code , globals(), clsdict)
        except:
            print(code)
            raise

    def __init__(rel, name, bases, clsdict):
        super(Relation1_to_all, rel).__init__(name, bases, clsdict)
        assert rel.__cinit__ and rel.__cfin__
        def init_sc(cls):
            if not hasattr(cls, "__psc__"):
                setattr(cls, "__psc__", DictSemiCocircuit())
        init_sc(rel.__cinit__)
        rel.__cinit__.__psc__.append(rel)
        init_sc(rel.__cfin__)
        rel.__cfin__.__nsc__.append(rel)
