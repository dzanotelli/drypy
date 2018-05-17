"""
.. module:: deputy
   :platform: Unix
   :synopsis: Sheriff-Deputy pattern decorator

.. moduleauthor:: Daniele Zanotelli <dazano@gmail.com>
"""

from . import get_status
from .sham import sham

class sheriff:
    """Decorator which makes drypy to run *func.deputy*
    instead of *func*.

    Example:
        >>> @sheriff()
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
       If you are dealing with methods, set `method=True` in
       your sheriff call:

       >>> class MyClass:
       ...     @sheriff(method=True)
       ...     def my_method(self, arg):
       ...         pass

    """

    def __init__(self, method=False):
        if type(method) is not bool:
            raise TypeError("method is not bool")

        self._method = method
        self._deputy_func = None

    def __call__(self, func, *args, **kwargs):
        """Return a decorator which will exec the original
        function/method if dryrun is set to False or run
        the deputy function/method otherwise. If deputy is
        not set the decorator will fallback to sham behaviour.

        """
        # keep a sheriff ref
        this = self

        if self._method:
            def decorator(self, *args, **kw):
                # if dryrun is disabled exec the original method
                if get_status() is False:
                    return func(self, *args, **kw)

                # dryrun on: exec deputy method
                if this._deputy_func:
                    return this._deputy_func(self, *args, **kw)

                # no deputy: fallback on sham
                sham_decorator = sham(method=True)(func)
                return sham_decorator(self, *args, **kw)
        else:
            def decorator(*args, **kw):
                # if dryrun is disabled exec the original function
                if get_status() is False:
                    return func(*args, **kw)

                # dryrun on: exec deputy function
                if this._deputy_func:
                    return this._deputy_func(*args, **kw)

                ## no deputy: fallback on sham
                sham_decorator = sham(method=False)(func)
                return sham_decorator(*args, **kw)

        decorator.deputy = this._set_deputy
        return decorator

    def _set_deputy(self, deputy_func):
        """Mark the *sheriff* substitute.

        Args:
            deputy_func: The function drypy will run in place of *sheriff*.

        Returns:
            *deputy_func* itself.
        """
        # func must be a callable
        if not getattr(deputy_func, '__call__', None):
            msg = "{} object is not a callable"
            msg = msg.format(type(deputy_func).__name__)
            raise TypeError(msg)

        self._deputy_func = deputy_func
        return deputy_func
