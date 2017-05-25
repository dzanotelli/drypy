from . import version

def get_version():
    return version._version

# dryrun switcher
_mode = False

def get_mode():
    return _mode

def set_mode(value):
    global _mode
    if type(value) is not bool:
        raise TypeError("Boolean required")
    _mode = value

def toggle_mode():
    if get() is True:
        set_mode(False)
    else:
        set_mode(True)
