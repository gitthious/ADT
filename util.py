# -*- coding: utf-8 -*-
"""
Created on Fri Sep 04 19:54:28 2015

@author: Thierry
"""

from functools import wraps

#def wrap_method(cls, wrapped_method_name, function, *args, **kargs):
##    @decorator    
#    def wrapper(obj, *args, **kargs):
#        function(obj, *args, **kargs)
#        return wrapped_method(obj,*args, **kargs)
#    if hasattr(cls, wrapped_method_name):
#        wrapped_method = getattr(cls, wrapped_method_name)
##        setattr(cls, wrapped_method_name, wrapper(wrapped_method)(*args, **kargs))
#        setattr(cls, wrapped_method_name, wraps(wrapped_method, assigned=[])(wrapper))
#    else:
#        setattr(cls, wrapped_method_name, function)
#    
#from decorator import decorator

from operator import itemgetter
from itertools import groupby

def groups_of_continuous_numbers(L):
    # see recipe in http://stackoverflow.com/questions/2154249/identify-groups-of-continuous-numbers-in-a-list
    return [map(itemgetter(1), g) for k, g in groupby(enumerate(L), lambda (i,x):i-x)]
# print f((1, 3, 4, 5, 8,9, 10, 11, 100,101))
# >>> [[1], [3, 4, 5], [8, 9, 10, 11], [100, 101]]

def extensionmethod(cls, name=None, decorator=None, alias=None, new_name=None):
    """Function decorator that extends base with the decorated
    function.

    Keyword arguments:
    :param T base: Base class to extend with method
    :param string name: Name of method to set
    :param Callable decorator: Additional decorator e.g staticmethod

    :returns: A function that takes the class to be decorated.
    :rtype: func -> func
    """

    def inner(func):
        """This function is returned by the outer extensionmethod()

        :param types.FunctionType func: Function to be decorated
        """

        func_names = [name or func.__name__]
        if alias:
            aliases = alias if isinstance(alias, list) else [alias]
            func_names += aliases

        func = decorator(func) if decorator else func

        for func_name in func_names:
            if new_name:
                setattr(cls, new_name, getattr(cls, func_name))
            setattr(cls, func_name, func)
        return func
    return inner


def extensionclassmethod(cls, name=None, alias=None):
    """Function decorator that extends base with the decorated
    function as a class method.

    Keyword arguments:
    :param T base: Base class to extend with classmethod
    :param string name: Name of method to set

    :returns: A function that takes the class to be decorated.
    :rtype: func -> func
    """

    return extensionmethod(cls=cls, name=name, decorator=classmethod,
                           alias=alias)

if __name__ == "__main__":
    import unittest
    class Test(unittest.TestCase):
        def test_extended_method_lambda(self):
            class X:
                pass
            @extensionmethod(X, alias="m")
            def f(self, a):
                return a
            x = X()
            self.assertEqual(x.f(2), 2)
            self.assertEqual(x.m(3), 3)

        def test_extended_undefined_method_init(self):
            class X:
                pass
            @extensionmethod(X, '__init__')
            def init(self):    
                self.i = 1
            x = X()
            self.assertEqual(x.i, 1)

        def test_extended_redefined_method_init(self):
            class X(object):
                def __init__(self):
                    self.a = 2        
            @extensionmethod(X, '__init__', new_name="init")
            def init(self,i):
                self.i = i
                self.init()
            x = X(1)
            self.assertEqual(x.i, 1)
            self.assertEqual(x.a, 2)

        def test_extended_classmethod(self):
            class X(object):
                def __init__(self, a):
                    self.a = a        
            @extensionclassmethod(X,'create')
            def create(cls):
                return cls(4)
            x = X.create()
            self.assertEqual(x.a, 4)
    
    unittest.main()

