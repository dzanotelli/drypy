"""
.. module:: utils
   :platform: Unix
   :synopsis: Miscellaneous utils

.. moduleauthor:: Daniele Zanotelli <dazano@gmail.com>
"""

import logging

logger = logging.getLogger(__name__)


def log_call(func, *args, **kw):
    """Produce a info message which logs the *func* call.

    """
    # concatenate args and kw args transforming string values
    # from 'value' to '"value"' in order to pretty display em
    func_args = []

    # concatenate positional args
    args = list(args)
    if args:
        for i, arg in enumerate(args):
            if type(arg) is str:
                args[i] = '"{}"'.format(arg)
        func_args.extend([str(arg) for arg in args])

    # concatenate non positional args
    if kw:
        for key, value in kw.items():
            if type(value) is str:
                kw[key] = '"{}"'.format(value)

        func_args.extend(["{k}={v}".format(k=k, v=v) for k, v in kw.items()])

    # print the log message
    msg = "[DRYRUN] call to '{func}({args})'"
    msg = msg.format(func=func.__name__, args=", ".join(func_args))
    logger.info(msg)
