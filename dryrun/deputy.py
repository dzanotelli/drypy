# (C) 2017 - Daniele Zanotelli
#            dazano [at] gmail [dot] com
#

from . import get_mode
from .simple import simple


class sheriff(simple):
    def __init__(self, func):
        self.function = func
        self.deputy_function = None

    def __call__(self, *args, **kwargs):
        # if dry run is disabled exec the original function
        if get_mode() is False:
            return self.function(*args, **kwargs)

        if not self.deputy_function:
            return super().__call__(*args, **kwargs)
        else:
            return self.deputy_function(*args, **kwargs)

    def deputy(self, dep):
        self.deputy_function = dep
        return dep
