================================================================
InVEST: Integrated Valuation of Ecosystem Services and Tradeoffs 
================================================================

.. image:: http://builds.naturalcapitalproject.org/buildStatus/icon?job=invest-nightly-develop
  :target: http://builds.naturalcapitalproject.org/job/invest-nightly-develop

About  InVEST
=============

InVEST (Integrated Valuation of Ecosystem Services and Tradeoffs) is a family
of tools for quantifying the values of natural capital in clear, credible, and
practical ways. In promising a return (of societal benefits) on investments in
nature, the scientific community needs to deliver knowledge and tools to
quantify and forecast this return. InVEST enables decision-makers to quantify
the importance of natural capital, to assess the tradeoffs associated with
alternative choices, and to integrate conservation and human development.

Older versions of InVEST ran as script tools in the ArcGIS ArcToolBox environment,
but have almost all been ported over to a purely open-source python environment.

InVEST is licensed under a permissive, modified BSD license.

For more information, see:
  * `InVEST API documentation <http://invest.readthedocs.io/>`_
  * InVEST on `bitbucket <https://bitbucket.org/natcap/invest>`__
  * The `Natural Capital Project website <http://naturalcapitalproject.org>`__.


.. Everything after this comment will be included in the API docs.
.. START API

Installing InVEST
=================

Python Dependencies
-------------------

Dependencies for ``natcap.invest`` are listed in ``requirements.txt``:

.. These dependencies are listed here statically because when I push the
   readme page to PyPI, they won't render if I use the .. include::
   directive.  Annoying, but oh well.  It just means that we'll need to
   periodically check that this list is accurate.

.. code-block::

{requirements}

Additionally, a python binding for Qt is needed to use the InVEST GUI, but is
not required for development against ``natcap.invest``.  InVEST uses the
interface library ``qtpy`` to support ``PyQt4``, ``PyQt5``, and ``PySide``.
One of these bindings for Qt must be installed in order to use the GUI.


Installing from Source
----------------------

If you have a compiler installed and configured for your system, and
dependencies installed, the easiest way to install InVEST as a python package 
is:

.. code-block:: console

    $ pip install natcap.invest


Installing the latest development version
-----------------------------------------

The latest development version of InVEST can be installed from our source tree:

.. code-block:: console

    $ pip install hg+https://bitbucket.org/natcap/invest@develop


Usage
=====

To run an InVEST model from the command-line, use the ``invest`` cli single
entry point:

.. code-block:: console

    $ invest --help
    usage: invest [-h] [--version] [-v | --debug] [--list] [-l] [-d [DATASTACK]]
                  [-w [WORKSPACE]] [-q] [-y] [-n]
                  [model]

    Integrated Valuation of Ecosystem Services and Tradeoffs. InVEST (Integrated
    Valuation of Ecosystem Services and Tradeoffs) is a family of tools for
    quantifying the values of natural capital in clear, credible, and practical
    ways. In promising a return (of societal benefits) on investments in nature,
    the scientific community needs to deliver knowledge and tools to quantify and
    forecast this return. InVEST enables decision-makers to quantify the
    importance of natural capital, to assess the tradeoffs associated with
    alternative choices, and to integrate conservation and human development.
    Older versions of InVEST ran as script tools in the ArcGIS ArcToolBox
    environment, but have almost all been ported over to a purely open-source
    python environment.
    
    positional arguments:
      model                 The model/tool to run. Use --list to show available
                            models/tools. Identifiable model prefixes may also be
                            used. Alternatively,specify "launcher" to reveal a
                            model launcher window.
    
    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      -v, --verbose         Increase verbosity. Affects how much is printed to the
                            console and (if running in headless mode) how much is
                            written to the logfile.
      --debug               Enable debug logging. Alias for -vvvvv
      --list                List available models
      -l, --headless        Attempt to run InVEST without its GUI.
      -d [DATASTACK], --datastack [DATASTACK]
                            Run the specified model with this datastack
      -w [WORKSPACE], --workspace [WORKSPACE]
                            The workspace in which outputs will be saved
    
    gui options:
      These options are ignored if running in headless mode
    
      -q, --quickrun        Run the target model without validating and quit with
                            a nonzero exit status if an exception is encountered
    
    headless options:
      -y, --overwrite       Overwrite the workspace without prompting for
                            confirmation
      -n, --no-validate     Do not validate inputs before running the model.
 



To list the available models:

.. code-block:: console 

    $ invest --list


Development
===========

Dependencies for developing InVEST are listed in ``requirements.txt`` and in
``requirements-dev.txt``.

Support
=======

Participate in the NatCap forums here:
http://forums.naturalcapitalproject.org

Bugs may be reported at http://bitbucket.org/natcap/invest
