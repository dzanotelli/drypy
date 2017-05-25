# (C) 2017 - Daniele Zanotelli
#            dazano [at] gmail [dot] com
#

from . import get_mode

class simple:
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        # if dry run is disabled exec the original function
        if get_mode() is False:
            return self.function(*args, **kwargs)

        func_args = []
        if args:
            func_args.extend([str(arg) for arg in args])
        if kwargs:
            func_args.extend(["{k}={v}".format(k=k, v=v)
                              for k, v in kwargs.items()])

        msg = "[DRY-RUN] call to '{func}({args})'"
        msg = msg.format(func=self.function.__name__,
                         args=", ".join(func_args))

        print(msg) # FIXME replace with logger
        return None
