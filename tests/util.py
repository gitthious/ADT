# -*- coding: utf-8 -*-

import unittest
from ADT.util import *
from ADT import hbds
import warnings

class TestCache(unittest.TestCase):
            
    def test_add_cache(self):
        cache = Cache()
        class X(metaclass=hbds.Class):
            i = 1
        x1 = X()
        x1.i = 2
        cache.add(x1)
        self.assertEqual(len(cache), 1)
        self.assertIn(x1, cache)
        x1.i = 3
        x2 = X()
        x2.i = 4
        x3 = X()
        x3.i = 5
        cache.add(x3)
        self.assertEqual(len(cache), 2)

        with warnings.catch_warnings(record=True) as w:
            # Trigger a warning.
            x3.i = 6
            # Verify some things
            self.assertEqual(len(w), 2)
##            assert issubclass(w[-1].category, DeprecationWarning)
##            assert "deprecated" in str(w[-1].message)

        self.assertEqual(x3.i, 6)

        x1.i = 7
        self.assertEqual(x1.i, 7)

        cache.remove(x1)
        self.assertEqual(len(cache), 1)

        cache.remove(x3)
        self.assertEqual(len(cache), 0)
        
    def test_cache_redefined_update(self):
        class X(metaclass=hbds.Class):
            i = 1
        fset = X.__setattr__
        class CacheTest(Cache):
            # we redefined before and after metthids for tests
            def before_setattr(cache, obj, attr, old_value):
                self.before = (obj, attr, old_value)
            def after_setattr(cache, obj, attr, new_value):
                self.after = (obj, attr, new_value)

        cache = CacheTest()
        x1 = X()
        x1.i = 2
        cache.add(x1)
        self.assertEqual(len(cache), 1)
        self.assertIn(x1, cache)
        x1.i = 3
        self.assertTupleEqual(self.before, (x1,'i', 2))
        self.assertTupleEqual(self.after, (x1,'i', 3))
        x2 = X()
        x2.i = 4
        x3 = X()
        x3.i = 5
        cache.add(x3)
        self.assertEqual(len(cache), 2)

        # no warning have generated
        with warnings.catch_warnings(record=True) as w:
            x3.i = 6
            self.assertEqual(len(w), 0)

        self.assertEqual(x3.i, 6)
        self.assertTupleEqual(self.before, (x3,'i', 5))
        self.assertTupleEqual(self.after, (x3,'i', 6))

        x1.i = 7
        self.assertEqual(x1.i, 7)
        self.assertTupleEqual(self.before, (x1,'i', 3))
        self.assertTupleEqual(self.after, (x1,'i', 7))

        cache.remove(x1)
        self.assertEqual(len(cache), 1)

        cache.remove(x3)
        self.assertEqual(len(cache), 0)

        x3.i = 12
        self.assertEqual(len(cache), 0)
        self.assertIs( X.__setattr__, fset)

        class Y: pass
        y = Y()
        cache.add(y)
        y.s = "y"
        self.assertEqual(len(cache), 1)
        self.assertTupleEqual(self.before, (y,'s', None))
        self.assertTupleEqual(self.after, (y,'s', "y"))

        
    def test_with_2_caches(self):
        class X(metaclass=hbds.Class):
            i = 1
        class CacheTest(Cache):
            # we redefined before and after methods for tests
            def before_setattr(cache, obj, attr, old_value):
                if cache is self.C1:
                    self.before1 = (obj, attr, old_value)
                else:
                    self.before2 = (obj, attr, old_value)

            def after_setattr(cache, obj, attr, new_value):
                if cache is self.C1:
                    self.after1 = (obj, attr, new_value)
                else:
                    self.after2 = (obj, attr, new_value)

        self.C1 = CacheTest()
        self.C2 = CacheTest()

        x1 = X()
        self.C1.add(x1);
        self.C2.add(x1)
        x1.i = 2
        self.assertEqual(x1.i, 2)
        self.assertTupleEqual(self.before1, (x1,'i', 1))
        self.assertTupleEqual(self.after1, (x1,'i', 2))
        self.assertTupleEqual(self.before2, (x1,'i', 1))
        self.assertTupleEqual(self.after2, (x1,'i', 2))
        self.C2.remove(x1)
        x1.i = 3
        self.assertEqual(x1.i, 3)
        self.assertTupleEqual(self.before1, (x1,'i', 2))
        self.assertTupleEqual(self.after1, (x1,'i', 3))
        # before 2 not change
        self.assertTupleEqual(self.before2, (x1,'i', 1))
        self.assertTupleEqual(self.after2, (x1,'i', 2))
        self.C1.remove(x1)
        x1.i = 4
        self.assertEqual(x1.i, 4)
        # before 1 not change
        self.assertTupleEqual(self.before1, (x1,'i', 2))
        self.assertTupleEqual(self.after1, (x1,'i', 3))
        # before 2 not change
        self.assertTupleEqual(self.before2, (x1,'i', 1))
        self.assertTupleEqual(self.after2, (x1,'i', 2))

    def test_relations(self):                        
        class X(metaclass=hbds.Class):
            x = 1
        class Y(metaclass=hbds.Class):
            y = "a"
        R = hbds.Link(X, 'R', Y)
        cache = Cache()
        x = X()
        cache.add(x)
        y = Y()
        r = R(x,y)
        R.cut(r)
        
def load_tests(loader, standard_tests, pattern):
    # add new doctest tests
    import doctest
    from ADT import util
    standard_tests.addTests(doctest.DocTestSuite(util))
    return standard_tests

if __name__ == "__main__":
    unittest.main(verbosity=2,
##        defaultTest=("TestCache.test_with_2_caches",)
        )

