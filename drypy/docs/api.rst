API
===

drypy
-----

The package provides some basic function to turn on/off the dryrun mode.

.. automodule:: drypy
   :members:

sham.py
-------

This module provide a basic decorator to make your function log the call instead
of executing.

.. automodule:: drypy.sham
   :members:

deputy.py
---------

The deputy module provides the *sheriff* decorator to mark your function. The
substitue function marked by *sheriff.deputy* will be run in place of the
original one. If no *deputy* is provided, *sheriff* will fall back to
*drypy.sham.sham*.

.. automodule:: drypy.deputy
   :members:
