# (C) 2017 - Daniele Zanotelli
#            dazano [at] gmail [dot] com
#

import logging
from . import get_status

logger = logging.getLogger(__name__)


class sham:
    """
    *decorator*: instead of executing the original function
    make drypy to log the call:

        >>> foo(bar, baz=42)
        [DRYRUN] call to 'foo(bar, baz=42)'
    """
    def __init__(self, func):
        self.function = func

    def __call__(self, *args, **kwargs):
        # if dry run is disabled exec the original function
        if get_status() is False:
            return self.function(*args, **kwargs)

        func_args = []
        if args:
            func_args.extend([str(arg) for arg in args])
        if kwargs:
            func_args.extend(["{k}={v}".format(k=k, v=v)
                              for k, v in kwargs.items()])

        msg = "[DRYRUN] call to '{func}({args})'"
        msg = msg.format(func=self.function.__name__,
                         args=", ".join(func_args))

        logger.info(msg)
        return None