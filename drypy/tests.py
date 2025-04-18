"""
.. module:: tests
   :platform: Unix
   :synopsis: drypy unittest

.. moduleauthor:: Daniele Zanotelli <dazano@gmail.com>
"""

import logging
import unittest

import drypy

from drypy import dryrun, toggle_dryrun
from drypy.patterns import sham, sheriff, sentinel
from .test_utils import DryPyTestCase


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


@sentinel(return_value=789)
def a_sentinel_function():
    """Just a function decorated by sentinel.

    """
    return 123


class AClass:
    """A Class with some methods to be decorated.

    """

    @sham
    def a_method(self, i, n=1):
        return i * n

    @sham(custom_msg="Antani")
    def another_method(self, i, n=1):
        return i * n

    @sham(return_value=789)
    def a_method_with_custom_return_value(self, i, n=1):
        return i * n

    @sham(log_level=logging.DEBUG)
    def a_method_with_debug_log(self, i, n=1):
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

    @sentinel(return_value="I am Sakshi. Skipper of the ship.")
    def a_sentinel_method(self):
        return "I am a sentinel method"

class TestModeSwitcher(DryPyTestCase):
    """Test the drypy switcher setting mode on/off

    """

    def test_get_status(self):
        # bad manual assignment will make 'get_status' to reset to False
        drypy._dryrun = 'pippo'
        self.assertEqual(dryrun(), False)

    def test_dryrun_set_on(self):
        dryrun(True)
        self.assertEqual(dryrun(), True)

    def test_dryrun_set_off(self):
        dryrun(False)
        self.assertEqual(dryrun(), False)

    def test_dryrun_toggle_from_off(self):
        dryrun(False)
        toggle_dryrun()
        self.assertEqual(dryrun(), True)

    def test_dryrun_toggle_from_on(self):
        dryrun(True)
        toggle_dryrun()
        self.assertEqual(dryrun(), False)


class TestShamDecorator(DryPyTestCase):
    """Test the 'sham' decorator

    """
    def test_a_function_dryrun_off(self):
        dryrun(False)
        self.assertEqual(a_function(), True)

    def test_a_function_dryrun_on(self):
        dryrun(True)
        self.assertEqual(a_function(), None)

    def test_a_method_dryrun_off(self):
        dryrun(False)
        an_instance = AClass()
        self.assertEqual(an_instance.a_method(10, 2), 20)

    def test_a_method_dryrun_on(self):
        dryrun(True)
        an_instance = AClass()
        self.assertEqual(an_instance.a_method(10, 2), None)

    def test_func_custom_log_message(self):
        @sham(custom_msg="Antani")
        def do_some():
            return True

        dryrun(True)

        with self.assertLogs('', level='INFO') as cm:
            self.assertEqual(do_some(), None)

        self.assertEqual(len(cm.records), 1)
        log_record = cm.records[0]
        self.assertEqual(log_record.levelno, logging.INFO)
        self.assertIn("Antani", log_record.getMessage())

    def test_func_logging_level(self):
        self.assertEqual(drypy.get_logging_level(), logging.INFO)

        @sham(log_level=logging.DEBUG)
        def do_something():
            return True

        dryrun(True)
        with self.assertNoLogs('root', level='INFO') as cm:
            self.assertEqual(do_something(), None)

        with self.assertLogs('root', level='DEBUG') as cm:
            self.assertEqual(do_something(), None)

        self.assertEqual(len(cm.records), 1)
        log_record = cm.records[0]
        self.assertEqual(log_record.levelno, logging.DEBUG)

    def test_func_return_value(self):
        @sham(return_value=789)
        def do_something():
            return True

        self.assertEqual(do_something(), True)
        dryrun(True)
        self.assertEqual(do_something(), 789)

    def test_method_custom_log_message(self):
        an_instance = AClass()
        dryrun(True)

        with self.assertLogs('', level='INFO') as cm:
            self.assertEqual(an_instance.another_method(10, 2), None)

        self.assertEqual(len(cm.records), 1)
        log_record = cm.records[0]
        self.assertEqual(log_record.levelno, logging.INFO)
        self.assertIn("Antani", log_record.getMessage())

    def test_method_logging_level(self):
        an_instance = AClass()
        self.assertEqual(drypy.get_logging_level(), logging.INFO)

        dryrun(True)
        with self.assertNoLogs('root', level='INFO') as cm:
            self.assertEqual(
                an_instance.a_method_with_debug_log(10, 2), None
            )

        with self.assertLogs('root', level='DEBUG') as cm:
            self.assertEqual(
                an_instance.a_method_with_debug_log(10, 2), None
            )

        self.assertEqual(len(cm.records), 1)
        log_record = cm.records[0]
        self.assertEqual(log_record.levelno, logging.DEBUG)

    def test_method_return_value(self):
        an_instance = AClass()

        self.assertEqual(
            an_instance.a_method_with_custom_return_value(10, 2), 20)
        dryrun(True)
        self.assertEqual(
            an_instance.a_method_with_custom_return_value(10, 2), 789
        )


class TestSheriffDeputyDecorator(DryPyTestCase):
    """Test the sheriff-deputy pattern.

    """

    def test_sheriff_without_deputy_dryrun_off(self):
        dryrun(False)
        self.assertEqual(a_sheriff_without_deputy(42), 'truth!')

    def test_sheriff_without_deputy_dryrun_on(self):
        dryrun(True)
        self.assertEqual(a_sheriff_without_deputy("some value"), None)

    def test_another_function_dryrun_off(self):
        dryrun(False)
        self.assertEqual(another_function(1, 2), 123)

        # check that deputy function is still callable
        self.assertEqual(dryrun_another_function(1, 2), 321)

    def test_another_function_dryrun_on(self):
        dryrun(True)
        result = another_function(1, 2)
        self.assertEqual(result, 321)

        # check that sheriff result is equal to deputy result
        deputy_result = dryrun_another_function(1, 2)
        self.assertEqual(result, deputy_result)

    def test_a_sheriff_without_deputy_dryrun_off(self):
        dryrun(False)
        an_instance = AClass()
        result = an_instance.a_sheriff_without_deputy(40, 2)
        self.assertEqual(result, 42)

    def test_a_sheriff_without_deputy_dryrun_on(self):
        dryrun(True)
        an_instance = AClass()
        result = an_instance.a_sheriff_without_deputy(40, 2)
        self.assertEqual(result, None)

    def test_a_sheriff_deputy_dryrun_off(self):
        dryrun(False)
        an_instance = AClass()
        result = an_instance.a_sheriff('world')
        self.assertEqual(result, 'hello world')

        # check also the deputy in order to verify it is still callable
        deputy_result = an_instance.a_sheriff_deputy('zxc')
        self.assertEqual(deputy_result, "goodbye world ..")

    def test_a_sheriff_deputy_dryrun_on(self):
        dryrun(True)
        an_instance = AClass()
        result = an_instance.a_sheriff('world')
        self.assertEqual(result, "goodbye world ..")

        # deputy result must be the sheriff result
        deputy_result = an_instance.a_sheriff_deputy('zxc')
        self.assertEqual(deputy_result, result)

    def test_sheriff_deputy_func_with_same_name(self):
        dryrun(False)
        self.assertTrue(a_last_func())

        dryrun(True)
        self.assertFalse(a_last_func())

    def test_sheriff_deputy_method_with_same_name(self):
        instance = AClass()

        dryrun(False)
        self.assertEqual(instance.a_last_method(), "im the last sheriff")

        dryrun(True)
        self.assertEqual(instance.a_last_method(), "im the last deputy")


class TestSentinelDecorator(DryPyTestCase):
    """Test the 'sentinel' decorator

    """
    def test_a_sentinel_function_dryrun_off(self):
        dryrun(False)
        self.assertEqual(a_sentinel_function(), 123)

    def test_a_sentinel_function_dryrun_on(self):
        dryrun(True)
        self.assertEqual(a_sentinel_function(), 789)

    def test_a_sentinel_method_dryrun_off(self):
        dryrun(False)
        an_instance = AClass()
        self.assertEqual(
            an_instance.a_sentinel_method(),
            "I am a sentinel method"
        )

    def test_a_sentinel_method_dryrun_on(self):
        dryrun(True)
        an_instance = AClass()
        self.assertEqual(
            an_instance.a_sentinel_method(),
            "I am Sakshi. Skipper of the ship."
        )


class TestLoggingLevel(DryPyTestCase):
    def test_logging_level(self):
        # without setting the logging level, the default is INFO
        dryrun(True)
        with self.assertLogs('drypy', level='INFO') as cm:
            a_function()

        self.assertEqual(len(cm.records), 1)
        log_record = cm.records[0]
        self.assertEqual(log_record.levelno, logging.INFO)

        # now change the global logging level to DEBUG, to be able to
        # capture all the logs
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)

        # change drypy logging level
        drypy.set_logging_level(logging.DEBUG)
        with self.assertLogs('drypy', level='DEBUG') as cm:
            a_function()

        self.assertEqual(len(cm.records), 1)
        log_record = cm.records[0]
        self.assertEqual(log_record.levelno, logging.DEBUG)

        # change drypy logging level to ERROR
        drypy.set_logging_level(logging.ERROR)

        with self.assertLogs('drypy', level='DEBUG') as cm:
            a_function()

        self.assertEqual(len(cm.records), 1)
        log_record = cm.records[0]
        self.assertEqual(log_record.levelno, logging.ERROR)
