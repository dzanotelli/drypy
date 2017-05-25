# 2017 - python-dryrun
#
# Unittest
#

import unittest

from .simple import simple
from .deputy import sheriff

@simple
def a_function():
    return True

@sheriff
def another_function(one, two, three=None):
    return 123

@another_function.deputy
def dryrun_another_function(one, two, three=None):
    print("Custom dryrun substitute for 'another_function")
    return 321

@sheriff
def a_sheriff_which_fallbacks_to_simple():
    return True

class TestSimpleDecorator(unittest.TestCase):

    def test_a_function(self):
        self.assertEqual(a_function(), None)

    def test_another_function(self):
        self.assertEqual(another_function(1, 2), 321)


    def test_sheriff_fallback_simple(self):
        self.assertEqual(a_sheriff_which_fallbacks_to_simple(42), None)

if __name__ == "__main__":
    unittest.main()
