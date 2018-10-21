"""drypy - dryrun for python

.. moduleauthor:: Daniele Zanotelli <dazano@gmail.com>
"""

import logging
from . import version

logger = logging.getLogger(__name__)
_dryrun = False                           # dryrun switcher flag


def get_version(short=False):
    """Returns the current drypy version.

    Optional args:
        short (bool): If True return just "major.minor"

    Returns:
        A string with the current drypy version.

    """
    if short:
        # extract the first two parts of version (eg '1.2' from '1.2.3')
        return '.'.join(version._version.split('.')[:2])
    else:
        return version._version

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
    if get_status() is True:
        set_dryrun(False)
    else:
        set_dryrun(True)
