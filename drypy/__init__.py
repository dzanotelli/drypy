"""drypy - dryrun for python

.. moduleauthor:: Daniele Zanotelli <dazano@gmail.com>
"""

import logging


logger = logging.getLogger(__name__)
_dryrun = False
_logging_level = logging.INFO


def dryrun(state=None):
    """Return current dryrun mode, If *state* is provided
    activate/deactivate dryrun before returning the status

    Optional args:
        state (bool): Set dryrun mode to the desired state.
    Returns:
        bool

    """
    if state is not None:
        set_dryrun(state)
    return get_status()


def get_status():
    """Returns True if the dryrun system is active.

    Returns:
        True or False

    """
    if _dryrun not in (True, False):
        msg = "Don't manually change the _dryrun flag! Use 'set_dryrun' "
        msg += "instead. Dryrun set to False."
        logger.warning(msg)
        set_dryrun(False)
    return _dryrun


def set_dryrun(value):
    """Set the dryrun mode on or off.

    Args:
        value (bool): Mode to be in.

    """
    global _dryrun
    if type(value) is not bool:
        raise TypeError("Boolean required")
    _dryrun = value


def toggle_dryrun():
    """Toggle the current dryrun mode.

    """
    set_dryrun(not get_status())


def set_logging_level(level):
    """
    Set the logging level drypy will use by default.

    """
    global _logging_level
    if type(level) is not int:
        raise TypeError("Integer required")
    _logging_level = level


def get_logging_level():
    """
    Return the current logging level used by drypy

    """
    return _logging_level
