Quickstart
==========

Basic usage
-----------

Suppose we have a *foo* function which reads a *bar* argument and writes it
to file:

.. code-block:: python

   def foo(bar):
       with open("/tmp/antani.txt", "w") as f:
           f.write(bar)


Dryrun mode is easily achievable using the *sham* decorator:

.. code-block:: python

   from drypy.patterns import sham

   @sham
   def foo(bar, baz=False):
       ...

Turning on *drypy* it's enough to make it log the following message instead
of executing *foo*:

   >>> from drypy import dryrun
   >>> dryrun(True)
   >>> foo(42)
   [DRYRUN] call to 'foo(42)'

.. note::

   *drypy* uses the python standard :py:mod:`logging` library therefore you
   will need to setup valid handlers in order to get the messages.

   *drypy* logs messages with the ``logging.INFO`` level.


Custom substitute
-----------------

Sometimes we may have complex situations we want to manage in a custom way
providing a complete substitute to the original function. The *sheriff-deputy*
pattern comes here in help:

.. code-block:: python

   from drypy.patterns import sheriff

   @sheriff
   def foo(bar):
       # do this and that
       pass

   @foo.deputy
   def foo(bar):
       # do this
       # DON'T do that
       # log a message
       pass

When *drypy* dryrun mode is set to **True**, the function marked by
*foo.deputy* will be executed in place of the fisrt defined *foo*.

.. important::

   Since the deputy function will receive the same args you are passing to the
   sheriff, it's advised that the two function signatures correspond.
   Otherwise, if you think that the sheriff function signature may change in
   the future, you can use the generic syntax `*args, **kw` for the deputy
   args.


Dryrun with mock
----------------

Sometimes we have a requirement to dryrun a function but also need to mock its
return value. The *sentinel* decorator can be used for this purpose:

.. code-block:: python

   from drypy.patterns import sentinel

   @sentinel(return_value=42)
   def foo(bar):
       return 12

Turning on *drypy* dryrun mode will now also mock the return value of *foo*
along with skipping execution and logging the call:

   >>> from drypy import dryrun
   >>> dryrun(True)
   >>> result = foo("anything")
   [DRYRUN] call to 'foo("anything")'
   >>> result
   42

.. note::

   *drypy* uses the python standard :py:mod:`logging` library therefore you
   will need to setup valid handlers in order to get the messages.

   *drypy* logs messages with the ``logging.INFO`` level.