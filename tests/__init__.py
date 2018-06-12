# -*- coding: utf-8 -*-

import unittest
import basictypes, fonctors, hbds

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for module in (basictypes, fonctors, hbds):
        tests = loader.loadTestsFromModule(module)
        suite.addTests(tests)
    return suite

                
if __name__ == '__main__':
    unittest.main()
