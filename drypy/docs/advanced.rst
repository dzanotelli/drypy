Advanced usage
==============

Apply decorators inline
-----------------------

Sometime you may need to activate just a particular call into your
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

and you need to give dryrun functionality just to the file writing thing.
Remember that decorators are just funcions (or classes) which get in input
an other function. Thus you can wrap it with either *sham*:

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

where :code:`self._deputy_of_write` should be defined with the same args of
:code:`f.write` or with :code:`*args, **kw`.

or *sentinel", and provide a return value:

.. code-block:: python

           # write it to file
           try:
               with open('file.txt', 'a') as f:
                   f.write = sentinel(return_value=None)(f.write)
                   f.write(result)
               ...

.. important::

    If you apply the decorator inline as in the following example:

    .. code-block::

       ...
       shutil.copy = sham(shutil.copy)
       ...

    be sure to call this block of code just once, or you may incur into a
    :code:`RecursionError: maximum recursion depth exceeded`. A good solution
    is to pack all the dryrun configuration in a specific function and call it
    when activating the dryrun mode:

    .. code-block::

       def setup_dryrun():
           ...
           shutil.copy = sham(shutil.copy)
           ...

       if activate_dryrun:
           setup_dryrun()
           dryrun(True)