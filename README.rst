drypy - easy dryrun mode for Python
===================================

The module helps you to implement `dryrun` mode in your
Python projects with an easy switch 'on/off' feature.

Authors: Daniele Zanotelli (dazano@gmail.com)

License: MIT

Documentation
-------------
.. _Sphinx: http://www.sphinx-doc.org/
.. _`project docs`: http://drypy.m240.it/docs/

The package is supplied with Sphinx_ compilable documentation
under the docs directory.

You can read the latest docs visiting the `project docs`_ online.



Basic usage
-----------

Apply the `sham` decorator to your function and set dryrun as on.

::

   import drypy
   from drypy.sham import sham

   @sham(method=False)
   def foo(bar):
       ...

   drypy.set_dryrun(True)

   foo(42)

Will log the following output:

::

   [DRYRUN] call to 'foo(42)'

using the python standard logging facility, thus it's up to you
to correctly configure it.

To use custom substitutes with specific beahviours please check the docs for the `sheriff-deputy` pattern.
