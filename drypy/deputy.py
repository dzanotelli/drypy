"""
.. module:: deputy
   :platform: Unix
   :synopsis: Sheriff-Deputy pattern decorator

.. moduleauthor:: Daniele Zanotelli <dazano@gmail.com>
"""

import logging
import functools
from . import get_status
from .sham import log_call

logger = logging.getLogger(__name__)


def sheriff(func):
    """Decorator which makes drypy to run *func.deputy*
    instead of *func*.

    Example:
        >>> @sheriff
        ... def woody():
        ...    print("I'm the Sheriff!")
        ...
        >>> @woody.deputy
        ... def woody():
        ...    print("I'm the Deputy!")
        ...
        ...
        >>> woody()
        I'm the Sheriff!
        >>> drypy.set_dryrun(True)
        >>> woody()
        I'm the Deputy!

    """
    @functools.wraps(func)
    def decorator(*args, **kw):
        # if dryrun is disabled exec the original method
        if get_status() is False:
            return func(*args, **kw)

        # dryrun on: exec deputy method
        deputy_func = getattr(decorator, 'deputy_callable', None)
        if callable(deputy_func):
            return deputy_func(*args, **kw)
        elif deputy_func is not None:
            logger.warning("Given deputy is not a callable, logging the call")

        # no deputy, log_call
        return log_call(func, *args, **kw)

    def set_deputy(func):
        setattr(decorator, 'deputy_callable', func)

        if func.__name__ == getattr(decorator, 'sheriff_name', None):
            return decorator
        else:
            return func

    setattr(decorator, 'deputy', set_deputy)
    setattr(decorator, 'sheriff_name', func.__name__)

    return decorator
