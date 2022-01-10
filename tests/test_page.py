import unittest
import doctest
from scrapekichiba import page

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(page))
    return tests