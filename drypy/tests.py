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

@sham()
def a_function():
    """Just a function decorated by sham.

    """
    return True

@sheriff()
def a_sheriff_which_fallbacks_to_sham(one):
    """Just a function decorated by sheriff with no deputy.
    It will fall back to sham.

    """
    return 'truth!' if one == 42 else False

@sheriff()
def another_function(one, two, three=None):
    """A third function decorated by sheriff; deputy follows.

    """
    return 123

@another_function.deputy
def dryrun_another_function(one, two, three=None):
    """The deputy which will be run in place of another_function.

    """
    return 321


class AClass:
    """A Class with some methods to be decorated.

    """

    @sham(method=True)
    def a_method(self, i, n=1):
        return i * n

    @sheriff(method=True)
    def a_sheriff_which_fallbacks_to_sham(self, one, two=3):
        return one + two

    @sheriff(method=True)
    def a_sheriff(self, foo, bar='hello'):
        return "{} {}".format(bar, foo)

    @a_sheriff.deputy
    def a_sheriff_deputy(self, foo, bar='hello'):
        return "goodbye world .."


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

    def test_bad_decorated_function(self):
        with self.assertRaises(TypeError):
            @sham(method='antani')
            def bad_decorated_func():
                pass

    def test_a_function_dryrun_off(self):
        drypy.set_dryrun(False)
        self.assertEqual(a_function(), True)

    def test_a_function_dryrun_on(self):
        drypy.set_dryrun(True)
        self.assertEqual(a_function(), None)

    def test_a_method_dryrun_off(self):
        drypy.set_dryrun(False)
        an_instance = AClass()
        self.assertEqual(an_instance.a_method(10, 2), 20)

    def test_a_method_dryrun_on(self):
        drypy.set_dryrun(True)
        an_instance = AClass()
        self.assertEqual(an_instance.a_method(10, 2), None)


class TestSheriffDeputyDecorator(unittest.TestCase):
    """Test the sheriff-deputy pattern.

    """

    def test_sheriff_fallback_sham_dryrun_off(self):
        drypy.set_dryrun(False)
        self.assertEqual(a_sheriff_which_fallbacks_to_sham(42), 'truth!')

    def test_sheriff_fallback_sham_dryrun_on(self):
        drypy.set_dryrun(True)
        self.assertEqual(a_sheriff_which_fallbacks_to_sham(42), None)

    def test_another_function_dryrun_off(self):
        drypy.set_dryrun(False)
        self.assertEqual(another_function(1, 2), 123)

        # check that deputy function is still callable
        self.assertEqual(dryrun_another_function(1, 2), 321)

    def test_another_function_dryrun_on(self):
        drypy.set_dryrun(True)
        result = another_function(1, 2)
        self.assertEqual(result, 321)

        # check that sheriff result is equal to deputy result
        deputy_result = dryrun_another_function(1, 2)
        self.assertEqual(result, deputy_result)

    def test_a_sheriff_which_fallbacks_to_sham_dryrun_off(self):
        drypy.set_dryrun(False)
        an_instance = AClass()
        result = an_instance.a_sheriff_which_fallbacks_to_sham(40, 2)
        self.assertEqual(result, 42)

    def test_a_sheriff_which_fallbacks_to_sham_dryrun_on(self):
        drypy.set_dryrun(True)
        an_instance = AClass()
        result = an_instance.a_sheriff_which_fallbacks_to_sham(40, 2)
        self.assertEqual(result, None)

    def test_a_sheriff_deputy_dryrun_off(self):
        drypy.set_dryrun(False)
        an_instance = AClass()
        result = an_instance.a_sheriff('world')
        self.assertEqual(result, 'hello world')

        # check also the deputy in order to verify it is still callable
        deputy_result = an_instance.a_sheriff_deputy('zxc')
        self.assertEqual(deputy_result, "goodbye world ..")

    def test_a_sheriff_deputy_dryrun_on(self):
        drypy.set_dryrun(True)
        an_instance = AClass()
        result = an_instance.a_sheriff('world')
        self.assertEqual(result, "goodbye world ..")

        # deputy result must be the sheriff result
        deputy_result = an_instance.a_sheriff_deputy('zxc')
        self.assertEqual(deputy_result, result)


if __name__ == "__main__":
    unittest.main()
