import unittest
import doctest
from scrapekichiba import const

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(const))
    return tests