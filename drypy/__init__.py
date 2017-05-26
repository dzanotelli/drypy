import logging
from . import version

logger = logging.getLogger(__name__)

def get_version():
    return version._version

# dryrun switcher
_dryrun = False

def get_status():
    if _dryrun not in (True, False):
        msg = "Don't manually change the _dryrun flag! Use 'set_dryrun' "
        msg += "instead. Dryrun set to False."
        logger.warning(msg)
        set_dryrun(False)
    return _dryrun

def set_dryrun(value):
    global _dryrun
    if type(value) is not bool:
        raise TypeError("Boolean required")
    _dryrun = value

def toggle_dryrun():
    if get_status() is True:
        set_dryrun(False)
    else:
        set_dryrun(True)
