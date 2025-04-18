import io
import logging
import os
import sys
import unittest

import drypy

# # capture emitted logs for further inspection. We use basicConfig
# # cos it auto formats messages on need with `LEVEL:..MESSAGE`
# # NOTE: basicConfig works just once! so it must be called here
# _emitted_logs = io.StringIO()
# logging.basicConfig(stream=_emitted_logs, level=logging.INFO)


class DryPyTestCase(unittest.TestCase):
    SILENT = True

    def setUp(self):
        if self.SILENT:
            # soppress output
            self._stdout = sys.stdout
            self._stderr = sys.stderr
            self._devnull = open(os.devnull, 'w')
            sys.stdout = self._devnull
            sys.stderr = self._devnull

        drypy.dryrun(False)
        self.reset_logging_conf()

    def reset_logging_conf(self):
        drypy.set_logging_level(logging.INFO)

    def tearDown(self):
        if self.SILENT:
            sys.stdout = self._stdout
            sys.stderr = self._stderr
            self._devnull.close()

        # reset logging config
        drypy.dryrun(False)
        self.reset_logging_conf()
