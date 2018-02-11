"""
.. module:: deputy
   :platform: Unix
   :synopsis: Sheriff-Deputy pattern decorator

.. moduleauthor:: Daniele Zanotelli <dazano@gmail.com>
"""

from . import get_status
from .sham import sham

class sheriff(sham):
    """Decorator which makes drypy to run *func.deputy*
    instead of *func*.

    Example:
        >>> @sheriff
        ... def my_func():
        ...    print("I'm the Sheriff!")
        ...
        >>> @my_func.deputy
        ... def my_other_func():
        ...    print("I'm the Deputy!")
        ...
        >>> my_func()
        I'm the Deputy!


    .. note::
       Providing a deputy is optional: when not provided drypy
       will automatically fallback on :class:`sham` behaviour.
    """
    def __init__(self, func):
        self.function = func
        self.deputy_function = None

    def __call__(self, *args, **kwargs):
        # if dryrun is disabled exec the original function
        if get_status() is False:
            return self.function(*args, **kwargs)

        # if deputy is defined use it, fallback to 'sham' otherwise
        if not self.deputy_function:
            return super().__call__(*args, **kwargs)
        else:
            return self.deputy_function(*args, **kwargs)

    def deputy(self, func):
        """Mark the *sheriff* substitute.

        Args:
            func: The function drypy will run in place of *sheriff*.

        Returns:
            *func* itself.
        """
        # func must be a callable
        if not getattr(func, '__call__', None):
            msg = "{} object is not a callable".format(type(func).__name__)
            raise TypeError(msg)

        self.deputy_function = func
        return func
