"""
.. module:: tests
   :platform: Unix
   :synopsis: drypy unittest

.. moduleauthor:: Daniele Zanotelli <dazano@gmail.com>
"""

import unittest
import logging
import drypy
from .sham import sham
from .deputy import sheriff

# disable messages
logging.disable(logging.CRITICAL)

@sham
def a_function():
    """Just a function decorated by sham.
    """
    return True

@sheriff
def a_sheriff_which_fallbacks_to_sham(one):
    """Just a function decorated by sheriff with no deputy.
    It will fall back to sham.
    """
    return True

@sheriff
def another_function(one, two, three=None):
    """A third function decorated by sheriff; deputy follows.
    """
    return 123

@another_function.deputy
def dryrun_another_function(one, two, three=None):
    """The deputy which will be run in place of another_function.
    """
    return 321


class TestModeSwitcher(unittest.TestCase):
    """Test the drypy switcher setting mode on/off
    """

    def test_get_status(self):
        # bad manual assignment will make 'get_status' to reset to False
        drypy._dryrun = 'pippo'
        self.assertEqual(drypy.get_status(), False)

    def test_dryrun_set_on(self):
        drypy.set_dryrun(True)
        self.assertEqual(drypy.get_status(), True)

    def test_dryrun_set_off(self):
        drypy.set_dryrun(False)
        self.assertEqual(drypy.get_status(), False)

    def test_dryrun_toggle_from_off(self):
        drypy.set_dryrun(False)
        drypy.toggle_dryrun()
        self.assertEqual(drypy.get_status(), True)

    def test_dryrun_toggle_from_on(self):
        drypy.set_dryrun(True)
        drypy.toggle_dryrun()
        self.assertEqual(drypy.get_status(), False)


class TestShamDecorator(unittest.TestCase):
    """Test the 'sham' decorator
    """
    def test_a_function_dryrun_off(self):
        drypy.set_dryrun(False)
        self.assertEqual(a_function(), True)

    def test_a_function_dryrun_on(self):
        drypy.set_dryrun(True)
        self.assertEqual(a_function(), None)


class TestSheriffDeputyDecorator(unittest.TestCase):
    """Test the sheriff+deputy decorator.
    """
    def test_sheriff_fallback_sham_dryrun_off(self):
        drypy.set_dryrun(False)
        self.assertEqual(a_sheriff_which_fallbacks_to_sham(42), True)

    def test_sheriff_fallback_sham_dryrun_on(self):
        drypy.set_dryrun(True)
        self.assertEqual(a_sheriff_which_fallbacks_to_sham(42), None)

    def test_another_function_dryrun_off(self):
        drypy.set_dryrun(False)
        self.assertEqual(another_function(1, 2), 123)

    def test_another_function_dryrun_on(self):
        drypy.set_dryrun(True)
        self.assertEqual(another_function(1, 2), 321)


if __name__ == "__main__":
    unittest.main()
