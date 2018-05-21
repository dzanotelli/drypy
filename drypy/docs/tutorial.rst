Tutorial
========

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

   from drypy.sham import sham

   @sham()
   def foo(bar, baz=False):
       ...

Turning on *drypy* it's enough to make it log the following message instead
of executing *foo*:

   >>> import drypy
   >>> drypy.set_dryrun(True)
   >>> foo(42)
   [DRYRUN] call to 'foo(42)'

.. note::
   *drypy* uses the python standard :py:mod:`logging` library therefore you
   will need to provide valid handlers to ``drypy.logger`` in order to get the
   messages.

   *drypy* logs messages with the ``logging.INFO`` level.

While writing custom classes the operation of directly decorating methods will
automatically affect all the future instances:

.. code-block:: python

           class MyClass:
               @sham(method=True)
               def my_method(self, arg, kw='antani'):
                   pass



Custom substitute
-----------------

Sometimes we may have complex situations we want to manage in a custom way,
providing a complete substitute to the original function. The *sheriff-deputy*
pattern comes here in help:

.. code-block:: python

   from drypy.deputy import sheriff

   @sheriff()
   def foo(bar):
       # do this and that
       pass

   @foo.deputy
   def foo_substitute(bar):
       # do this
       # DON'T do that
       # log a message
       pass

When *drypy* dryrun mode is set to **True**, *foo_substitute* will be executed
in place of *foo*.

.. important::

   While placing the custom substitute within the same namespace of the
   original function, remember to define the deputy with a different name. Not
   doing so, the deputy function will be always called in place of sheriff with
   no reguard of the dryrun on/off status.

Example:

..   code-block:: python

   class Pippo:
        @sheriff(method=True)
        def do(self):
            # never called
            print('foo')

        @do.deputy
        def do(self):
            # always called
            print('bar')

   drypy.set_dryrun(False)

This code block will always print `bar` even if dryrun is correctly set to
`False` because the deputy function is overriding the sheriff.


Advanced usage
--------------

Sometime you may need to activate just a particular standard call into your
function. Let's say we have something like:

.. code-block:: python

   class MyWriter:
       def read_db_and_write_result_to_file(self):
           # read something from database
           result = query_result()

           # write it to file
           try:
               with open('file.txt', 'a') as f:
                   f.write(result)
               return True
           except:
               return False

and you need to give dryrun functionality just to the file writing thing. You
can wrap it with either *sham*

.. code-block:: python

           # write it to file
           try:
               with open('file.txt', 'a') as f:
                   f.write = sham()(f.write)
                   f.write(result)
               ...

or *sheriff*, and provide a *deputy*:

.. code-block:: python

           # write it to file
           try:
               with open('file.txt', 'a') as f:
                   f.write = sheriff()(f.write)
                   f.write.deputy(self._deputy_of_write)
                   f.write(result)
               ...

.. note::

   Dealing with *staticmethods* your decorators should be called with
   `method=False` (it's actually the default thus there is no need to specify
   it). That's why in the example above sham and deputy decorators are called
   without the *method* argument.
