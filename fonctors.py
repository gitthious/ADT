# -*- coding: utf-8 -*-

"""
les foncteurs:
    ils prennent en entrée un objet ou un iterable
    ils retournent un itérable
    ils peuvent s'enchainer comme des pipes (| cad __or__)
    pour les classes
        OBJ
        PSC, NSC
        ATT
        INIT, FIN
    pour les instances
        OPSC, ONSC
        OATT
        CLASS (equivalent à type)
        OINIT, OFIN
    Les foncteurs serviront de base aux queries puis aux querietrees
    options: raise and stop or raise and continue

    ex:
       (X,) | OBJ | OPSC(R) | OFIN => mieux car introduit une nouvelle syntaxe pour un nx d'abstraction sup.
       X.OBJ.OPSC(R).OFIN

"""

import inspect, enum, warnings
from collections.abc import Iterable

def public_attrs_fromdict(dic):
    """
    Return all public names of *dic*.

    Public names do not begin with '_', are not function
    and are not *property*!
    """
    return [attr for attr in dic \
            if not attr.startswith('_') \
            and not inspect.isroutine(dic[attr]) \
            and not isinstance(dic[attr], property)]

def getattrsfromdict(dic):
    warnings.warn(
        "getattrsfromdict is deprecated, use public_attrs_fromdict(dict) instead.",
        DeprecationWarning,
        stacklevel=4,
    )
    return public_attrs_fromdict(dic)
    
def public_attrs(obj, follow_mro=True):
    """
    Return names of public attributes of *obj* throught class hierarchy and
    in respect of declaration order. If obj is a class, *names* are class attributes.
    """
    if obj in (object, type): return []
    obj_attrs = public_attrs_fromdict(obj.__dict__)
    class_attrs = []
    cls = obj if isinstance(obj, type) else type(obj)
    if follow_mro:
        try:
            class_attrs += public_attrs(cls.mro()[1], follow_mro)
        except TypeError: # If we want mro of class of class!
            pass
    class_attrs += public_attrs_fromdict(cls.__dict__)

    i =  0
    for a in class_attrs:
        if a in obj_attrs:
            i += 1
            continue
        obj_attrs.insert(i, a)
        i += 1

    return obj_attrs
    
def getattrs(obj, follow_mro=True):
    warnings.warn(
        "getattrs is deprecated, use public_attrs(...) instead.",
        DeprecationWarning,
        stacklevel=4,
    )
    return public_attrs(obj, follow_mro)


def to_iterable(obj):
    """Return obj as an imutable iterable if necessary, except for str.
       If obj is already an iterable, return obj unchanged.
    """
    if not isinstance(obj, Iterable) \
    or isinstance(obj, (str, bytes)) \
    or isinstance(obj, enum.EnumMeta): 
        return (obj,)
    return obj

# see https://www.peterbe.com/plog/fastest-way-to-uniquify-a-list-in-python-3.6
# and collections.Counter doc
# and essentially a pipe package in https://github.com/JulienPalard/Pipe
# You can read for more general purpose:
#   * www.dabeaz.com/generators/Generators.pdf
#   * http://www.dabeaz.com/tutorials.html in generators

from pipe import *

@Pipe
def CLASS(objects):
    """Return generator on types (or classes) of objects"""
    return (type(o) for o in objects)

@Pipe
def attrs(objects, follow_mro=True):
    """Return generator on all public attribute names of objects.
       By default, follow_mro is true to retreive all attributes throught
       classes herarchy (mro).
    """
    for obj in objects:
        for att in public_attrs(obj, follow_mro):
            yield att

@Pipe
def valattrs(objects, attrnames=[], follow_mro=True):
    """Return generator on all public attribute values of objects.
       By default, follow_mro is true to retreive all attributes throught
       classes herarchy (mro).
    """
    if len(attrnames) != 0:
        for obj in objects:
            for att in public_attrs(obj, follow_mro):
                if att not in attrnames: continue
                yield getattr(obj,att)
    else:
        for obj in objects:
            for att in public_attrs(obj, follow_mro):
                yield getattr(obj,att)
@Pipe           
def OBJOF(objects, *classes):
    """Return generator to filter objects that are instances of classes."""
    return (obj for obj in objects if isinstance(obj, classes))


