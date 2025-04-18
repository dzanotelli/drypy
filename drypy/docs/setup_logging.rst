Setup Logging
=============

Setup
-----

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


Configure custom logging level
------------------------------

By default, `drypy` emits logs with level `logging.INFO`.
You can set a custom log level using the `set_logging_level` function:

.. code-block:: python

    import logging
    from drypy import set_logging_level

    set_logging_level(logging.DEBUG)

This will affect all the logs emitted by `drypy`.

It's also possibile to set a specific log level for each decorated function
by using the :code:`log_level` argument on the :func:`drypy.patterns.sham`
decorator. This value overrides the global setting above.
Please refer to the API documentation for more details.

.. important::

    This function will affect just the level of emitted logs. Please ensure
    that both the :code:`drypy` logger and the attached handlers have a log
    level equal or lower to this level, otherwise they will filter out logs.
    Or leave them to :code:`logging.NOTSET` to rely on root logger
    configuration.
    E.g., setting :code:`set_logging_level(logging.WARNING)` and the
    :code:`drypy` logger to :code:`logging.ERROR` will produce no logs.
    Please refer to official python logging docs for more.
