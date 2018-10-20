"""
.. module:: sham
   :platform: Unix
   :synopsis: Basic decorator to implement dryrun

.. moduleauthor:: Daniele Zanotelli <dazano@gmail.com>
"""

import logging
import functools
from . import get_status

logger = logging.getLogger(__name__)


def sham(func):
    """Decorator which makes drypy to log the call of the target
    function without executing it.

    Example:
        >>> @sham
        ... def foo(bar, baz=None):
        ...     return 42
        ...
        >>> foo("sport", baz=False)
        42
        >>> foo("sport", baz=False)
        INFO:drypy.sham:[DRYRUN] call to 'foo(sport, baz=False)'

    """
    @functools.wraps(func)
    def decorator(*args, **kw):
        # if dry run is disabled exec the original method
        if get_status() is False:
            return func(*args, **kw)
        else:
            log_call(func, *args, **kw)
            return None
    return decorator

def log_call(func, *args, **kw):
    # concatenate args and kw args transforming string values
    # from 'value' to '"value"' for a pretty display
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
