# (C) 2017 - Daniele Zanotelli
#
# Unit Test
#

import unittest
import logging
import drypy
from .witness import witness
from .deputy import sheriff

# disable messages
logger = logging.getLogger(__name__)
logger.propagate = False

@witness
def a_function():
    return True

@sheriff
def a_sheriff_which_fallbacks_to_witness(one):
    return True

@sheriff
def another_function(one, two, three=None):
    return 123

@another_function.deputy
def dryrun_another_function(one, two, three=None):
    logger.info("[DRYRUN] Custom dryrun substitute for 'another_function'")
    return 321


class TestModeSwitcher(unittest.TestCase):
    """
    Test the drypy switcher to set mode (dryrun/not dryrun)
    """
    def test_get_status(self):
        drypy._dryrun = 'pippo'
        self.assertEqual(drypy.get_status(), False)

    def test_set_dryrun(self):
        drypy.set_dryrun(True)
        self.assertEqual(drypy.get_status(), True)

    def test_set_not_dryrun(self):
        drypy.set_dryrun(False)
        self.assertEqual(drypy.get_status(), False)

    def test_toggle_to_dryrun(self):
        drypy.set_dryrun(False)
        drypy.toggle_dryrun()
        self.assertEqual(drypy.get_status(), True)

    def test_toggle_to_not_dryrun(self):
        drypy.set_dryrun(True)
        drypy.toggle_dryrun()
        self.assertEqual(drypy.get_status(), False)


class TestWitnessDecorator(unittest.TestCase):
    """
    Test the 'witness' decorator
    """
    def test_a_function_dryrun_off(self):
        drypy.set_dryrun(False)
        self.assertEqual(a_function(), True)

    def test_a_function_dryrun_on(self):
        drypy.set_dryrun(True)
        self.assertEqual(a_function(), None)


class TestSheriffDeputyDecorator(unittest.TestCase):
    """
    Test the sheriff+deputy decorator.
    """
    def test_sheriff_fallback_witness_dryrun_off(self):
        drypy.set_dryrun(False)
        self.assertEqual(a_sheriff_which_fallbacks_to_witness(42), True)

    def test_sheriff_fallback_witness_dryrun_on(self):
        drypy.set_dryrun(True)
        self.assertEqual(a_sheriff_which_fallbacks_to_witness(42), None)

    def test_another_function_dryrun_off(self):
        drypy.set_dryrun(False)
        self.assertEqual(another_function(1, 2), 123)

    def test_another_function_dryrun_on(self):
        drypy.set_dryrun(True)
        self.assertEqual(another_function(1, 2), 321)


if __name__ == "__main__":
    unittest.main()
