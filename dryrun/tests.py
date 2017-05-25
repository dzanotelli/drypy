# 2017 - python-dryrun
#
# Unittest
#

import unittest

from . import set_mode
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
def a_sheriff_which_fallbacks_to_simple(one):
    return True

class TestSimpleDecorator(unittest.TestCase):

    def test_a_function_dryrun_off(self):
        set_mode(False)
        self.assertEqual(a_function(), True)

    def test_another_function_dryrun_off(self):
        set_mode(False)
        self.assertEqual(another_function(1, 2), 123)

    def test_sheriff_fallback_simple_dryrun_off(self):
        set_mode(False)
        self.assertEqual(a_sheriff_which_fallbacks_to_simple(42),True)

    def test_a_function_dryrun_on(self):
        set_mode(True)
        self.assertEqual(a_function(), None)

    def test_another_function_dryrun_on(self):
        set_mode(True)
        self.assertEqual(another_function(1, 2), 321)

    def test_sheriff_fallback_simple_dryrun_on(self):
        set_mode(True)
        self.assertEqual(a_sheriff_which_fallbacks_to_simple(42), None)

if __name__ == "__main__":
    unittest.main()
