"""
.. module:: tests
   :platform: Unix
   :synopsis: drypy unittest

.. moduleauthor:: Daniele Zanotelli <dazano@gmail.com>
"""

import unittest
import logging
import drypy
from drypy.sham import sham
from drypy.deputy import sheriff


@sham
def a_function():
    """Just a function decorated by sham.

    """
    return True

@sheriff
def a_sheriff_without_deputy(one):
    """Just a function decorated by sheriff with no deputy.
    It will fall back to sham.

    """
    return 'truth!' if one == 42 else False

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

@sheriff
def a_last_func():
    return True

@a_last_func.deputy
def a_last_func():
    return False


class AClass:
    """A Class with some methods to be decorated.

    """

    @sham
    def a_method(self, i, n=1):
        return i * n

    @sheriff
    def a_sheriff_without_deputy(self, one, two=3):
        return one + two

    @sheriff
    def a_sheriff(self, foo, bar='hello'):
        return "{} {}".format(bar, foo)

    @a_sheriff.deputy
    def a_sheriff_deputy(self, foo, bar='hello'):
        return "goodbye world .."

    @sheriff
    def a_last_method(self):
        return "im the last sheriff"

    @a_last_method.deputy
    def a_last_method(self):
        return "im the last deputy"


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

    def test_sheriff_without_deputy_dryrun_off(self):
        drypy.set_dryrun(False)
        self.assertEqual(a_sheriff_without_deputy(42), 'truth!')

    def test_sheriff_without_deputy_dryrun_on(self):
        drypy.set_dryrun(True)
        self.assertEqual(a_sheriff_without_deputy("some value"), None)

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

    def test_a_sheriff_without_deputy_dryrun_off(self):
        drypy.set_dryrun(False)
        an_instance = AClass()
        result = an_instance.a_sheriff_without_deputy(40, 2)
        self.assertEqual(result, 42)

    def test_a_sheriff_without_deputy_dryrun_on(self):
        drypy.set_dryrun(True)
        an_instance = AClass()
        result = an_instance.a_sheriff_without_deputy(40, 2)
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

    def test_sheriff_deputy_func_with_same_name(self):
        drypy.set_dryrun(False)
        self.assertTrue(a_last_func())

        drypy.set_dryrun(True)
        self.assertFalse(a_last_func())

    def test_sheriff_deputy_method_with_same_name(self):
        instance = AClass()

        drypy.set_dryrun(False)
        self.assertEqual(instance.a_last_method(), "im the last sheriff")

        drypy.set_dryrun(True)
        self.assertEqual(instance.a_last_method(), "im the last deputy")


if __name__ == "__main__":
    import io
    captured = io.StringIO()
    logging.basicConfig(stream=captured, level=logging.INFO)

    try:
        unittest.main()
    finally:
        captured.seek(0)
        print("\n---- CAPTURED LOGS ----")
        for line in captured.readlines():
            print(line)
