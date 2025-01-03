"""
.. module:: patterns
   :platform: Unix
   :synopsis: Decorators to implement dryrun

.. moduleauthor:: Daniele Zanotelli <dazano@gmail.com>
"""

import logging
import functools
from . import dryrun
from .utils import log_call

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
        if dryrun() is False:
            return func(*args, **kw)
        else:
            log_call(func, *args, **kw)
            return None
    return decorator


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
        if dryrun() is False:
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


def sentinel(return_value=None):
    """Decorator which makes drypy to log the call of the target
    function and returns a user defined value without executing it.

    Example 1:
        >>> @sentinel(return_value=25)
        ... def foo(bar, baz=None):
        ...     return 42
        ...
        >>> a = foo("sport", baz=False)
        >>> print(a)
        42
        >>> dryrun(True)
        >>> b = foo("sport", baz=False)
        INFO:drypy.sentinel:[DRYRUN] call to 'foo(sport, baz=False)'
        >>> print(b)
        25

    Example 2:
        >>> @sentinel(return_value="I am Sakshi")
        ... def sakfoo(bar):
        ...     return "I am sakfoo"
        ...
        >>> a = sakfoo("sport")
        >>> print(a)
        'I am sakfoo'
        >>> dryrun(True)
        >>> b = sakfoo("sport")
        INFO:drypy.sentinel:[DRYRUN] call to 'sakfoo(sport)'
        >>> print(b)
        'I am Sakshi'

    """
    # This is the decorator function, which accepts `return_value`
    def decorator(func):
        # This is the actual decorator
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # The wrapper executes based on the `dryrun` condition
            if dryrun() is False:
                return func(*args, **kwargs)
            else:
                log_call(func, *args, **kwargs)
                return return_value

        return wrapper

    return decorator  # Return the decorator function
