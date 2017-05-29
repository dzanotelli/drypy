import logging
from . import version

logger = logging.getLogger(__name__)

def get_version():
    """
    Return the current drypy version.
    """
    return version._version

# dryrun switcher
_dryrun = False

def get_status():
    """
    Return True if the dryrun system is active.
    """
    if _dryrun not in (True, False):
        msg = "Don't manually change the _dryrun flag! Use 'set_dryrun' "
        msg += "instead. Dryrun set to False."
        logger.warning(msg)
        set_dryrun(False)
    return _dryrun

def set_dryrun(value):
    """
    Set the dryrun on or off.
    """
    global _dryrun
    if type(value) is not bool:
        raise TypeError("Boolean required")
    _dryrun = value

def toggle_dryrun():
    """
    Toggle current dryrun status.
    """
    if get_status() is True:
        set_dryrun(False)
    else:
        set_dryrun(True)
