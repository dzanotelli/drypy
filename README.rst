drypy - easy dryrun mode for Python
===================================

The module helps you to implement `dryrun` mode in your
Python projects with an easy switch 'on/off' feature.

Authors: Daniele Zanotelli (dazano@gmail.com)
Copyright: 2017-2018
License: MIT
Python version: 3.x

Documentation
-------------
.. _Sphinx: http://www.sphinx-doc.org/
.. _`project docs`: http://drypy.m240.it/docs/

The package is supplied with Sphinx_ compilable documentation
under the docs directory.

You can read the latest docs visiting the `project docs`_ online.

Installation
------------

Via pip:

::
   $ pip install drypy

or download the project from the github and compile the package

::
   $ git clone https://github.com/dzanotelli/drypy.git
   $ cd drypy
   $ make whl

and you'll find your brand-new whl under the dist/ subdirectory.

Basic usage
-----------

Apply the `sham` decorator to your function and set dryrun as on.

::

   from drypy import dryrun
   from drypy.patterns import sham

   >>> @sham
   >>> def foo(bar):
           pass
   >>> dryrun(True)
   >>> foo(42)

Will log the following output:

::

   [DRYRUN] call to 'foo(42)'

using the python standard logging facility, thus it's up to you
to correctly configure it.

To use custom substitutes with specific beahviours please check the docs for the `sheriff-deputy` pattern.
