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
       IDENT(X) | OBJ | OPSC(R) | OFIN => mieux car introduit une nouvelle syntaxe pour un nx d'abstraction sup.
       X.OBJ.OPSC(R).OFIN

"""

import collections, inspect

def getattrsfromdict(dic):
    return [attr for attr in dic \
            if not attr.startswith('_') \
            and not inspect.isroutine(dic[attr])]
    
def getattrs(obj):
    return getattrsfromdict(dict(inspect.getmembers(obj)))

def to_iterable(obj):
    """Return obj as an inmutable iterable if necessary, except for str.
       If obj is already an iterable, return obj unchanged.
    """
    if not isinstance(obj, collections.Iterable) \
    or isinstance(obj, str): 
        return (obj,)
    return obj
    
class Fonctor(object):
    def __init__(self, func=None, *args, **kargs):
        self.__func = func if func is not None else lambda x: x
        self.__args = args
        self.__kargs = kargs
    def __or__(self, other):
        return self.__exec(other)
    def __ror__(self, other):
        return self.__exec(other)
    def __call__(self, *args, **kargs):
        self.__args = args
        self.__kargs = kargs
        return self
    def __exec(self, other):
        result = set()
        for l in [self.__func(o, *self.__args, **self.__kargs) for o in to_iterable(other)]:
            for o in to_iterable(l): result.add(o)            
        return result
        

IDENT = Fonctor()                          
CLASS = Fonctor(type)
attrs = Fonctor(getattrs)
valattrs = Fonctor(lambda obj: [getattr(obj,a) for a in getattrs(obj)])

    
