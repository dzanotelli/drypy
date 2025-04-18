import io
import logging
import os
import sys
import unittest


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

        # capture emitted logs for further inspection
        self._emitted_logs = io.StringIO()
        logging.basicConfig(stream=self._emitted_logs, level=logging.INFO)

    def get_emitted_logs(self):
        """
        Returns emitted logs not yet read

        """
        self._emitted_logs.seek(0)
        logs = self._emitted_logs.read()
        self._emitted_logs.truncate(0)
        self._emitted_logs.seek(0)
        return logs

    def tearDown(self):
        if self.SILENT:
            sys.stdout = self._stdout
            sys.stderr = self._stderr
            self._devnull.close()
