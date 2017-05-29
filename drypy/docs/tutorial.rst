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

   @sham
   def foo(bar, baz=False):
       ...

Turning on *drypy* it's enough to make it log the following message instead
of executing *foo*:

   >>> import drypy
   >>> drypy.set_dryrun(True)
   >>> foo(42)
   [DRYRUN] call to 'foo(42)'


Custom substitute
-----------------

Sometimes we may have complex situations we want to manage in a custom way,
providing a complete substitute to the original function. The *sheriff-deputy*
pattern comes here in help:

.. code-block:: python

   from drypy.deputy import sheriff

   @sheriff
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
                   f.write = sham(f.write)
                   f.write(result)
               ...

or *sheriff*, and provide a *deputy*:

.. code-block:: python

           # write it to file
           try:
               with open('file.txt', 'a') as f:
                   f.write = sheriff(f.write)
                   f.write.deputy(self._deputy_of_write)
                   f.write(result)
               ...
