Setup Logging
=============

`drypy` uses the standard python logging facility to display messages. Each
`drypy` module initializes its own logger using the standard syntax:

.. code-block:: python

    logger = logging.getLogger(__name__)

Therefore, it's enough to correctly configure the logger named `drypy` to get
the output.

Follows a working example:

.. code-block:: python

    import logging
    from drypy import dryrun
    from drypy.patterns import sham

    logger = logging.getLogger('drypy')
    logger.setLevel(logging.INFO)
    h = logging.StreamHandler()  # print to console
    h.setLevel(logging.INFO)
    logger.addHandler(h)

    @sham
    def do_something():
        print('hello')

    do_something()
    # now activate dryrun
    dryrun(True)
    do_something()

You should get the following output in your console:

.. code-block:: python

    hello
    [DRYRUN] call to 'do_something()'