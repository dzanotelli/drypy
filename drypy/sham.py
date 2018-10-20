"""
.. module:: sham
   :platform: Unix
   :synopsis: Basic decorator to implement dryrun

.. moduleauthor:: Daniele Zanotelli <dazano@gmail.com>
"""

import logging
from . import get_status

logger = logging.getLogger(__name__)


def sham(func):
    def decorator(*args, **kw):
        # if dry run is disabled exec the original method
        if get_status() is False:
            return func(*args, **kw)
        else:
            log_args(func, *args, **kw)
            return None
    return decorator

def log_args(func, *args, **kw):
    func_args = []

    # concatenate positional args
    if args:
        func_args.extend([str(arg) for arg in args])

    # concatenate non positional args
    if kw:
        func_args.extend(["{k}={v}".format(k=k, v=v) for k, v in kw.items()])

    # print the log message
    msg = "[DRYRUN] call to '{func}({args})'"
    msg = msg.format(func=func.__name__, args=", ".join(func_args))
    logger.info(msg)








class sham2:
    """Decorator which makes drypy to log the call of the target
    function without executing it.

    Example:
        >>> @sham()
        ... def foo(bar, baz=None):
        ...     pass
        ...
        >>> foo(bar, baz=42)
        INFO:drypy.sham:[DRYRUN] call to 'foo(bar, baz=42)'

    .. note::
       If you are dealing with bound methods, set `method=True` in
       your sham call:

       >>> class MyClass:
       ...     @sham(method=True)
       ...     def my_method(self, arg):
       ...         pass

    """
    def __call__(self, func):
        """Return a decorator which will exec the original
        function/method if dryrun is set to False or log
        the call otherwise.

        """
        def decorator(*args, **kwargs):
            # if dry run is disabled exec the original method
            if get_status() is False:
                return func(*args, **kwargs)
            else:
                self._log_args(func, *args, **kwargs)
                return None
        return decorator

    def _log_args(self, func, *args, **kw):
        func_args = []
        if args:
            func_args.extend([str(arg) for arg in args])
        if kw:
            func_args.extend(["{k}={v}".format(k=k, v=v)
                              for k, v in kw.items()])

        msg = "[DRYRUN] call to '{func}({args})'"
        msg = msg.format(func=func.__name__, args=", ".join(func_args))

        logger.info(msg)
