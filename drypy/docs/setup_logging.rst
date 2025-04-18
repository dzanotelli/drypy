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

`drypy` by default emit logs with level `logging.INFO`.
It's possible to set a custom level using the function `set_logging_level`:

.. code-block:: python

    import logging
    from drypy import set_logging_level

    set_logging_level(logging.DEBUG)

.. important::

    This function will affect just the level of emitted logs. Please ensure
    that both the :code:`drypy` logger and the attached handlers have a log
    level equal or lower to this level, otherwise they will filter out logs.
    E.g., setting :code:`set_logging_level(logging.WARNING)` and the
    :code:`drypy` logger to :code:`logging.ERROR` will produce no logs.
    Please refer to official python logging docs for more.
