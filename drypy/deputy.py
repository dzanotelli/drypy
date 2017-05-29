# (C) 2017 - Daniele Zanotelli
#            dazano [at] gmail [dot] com
#

from . import get_status
from .sham import sham

class sheriff(sham):
    def __init__(self, func):
        self.function = func
        self.deputy_function = None

    def __call__(self, *args, **kwargs):
        # if dryrun is disabled exec the original function
        if get_status() is False:
            return self.function(*args, **kwargs)

        # if deputy is defined use it, fallback to 'simple' otherwise
        if not self.deputy_function:
            return super().__call__(*args, **kwargs)
        else:
            return self.deputy_function(*args, **kwargs)

    def deputy(self, dep):
        # FIXME: check dep, must be a callable
        self.deputy_function = dep
        return dep
