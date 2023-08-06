
pl-pacscopy
===========

.. image:: https://badge.fury.io/py/pacscopy.svg
    :target: https://badge.fury.io/py/pacscopy

.. image:: https://travis-ci.org/FNNDSC/pacscopy.svg?branch=master
    :target: https://travis-ci.org/FNNDSC/pacscopy

.. image:: https://img.shields.io/badge/python-3.5%2B-blue.svg
    :target: https://badge.fury.io/py/pl-pacscopy

.. contents:: Table of Contents


Abstract
--------

``pacscopy`` is a simple plugin that copies data from open storage to create a new top level ChRIS Feed. It's core utility is in demonstrating how to create a largely trivial FS plugin/app for the ChRIS system.

Synopsis
--------

.. code::

    python pacscopy.py                                              \
        [-v <level>] [--verbosity <level>]                          \
        [-d <dir>] [--dir <dir>]                                    \
        [--version]                                                 \
        [--man]                                                     \
        [--meta]                                                    \
        <outputDir> 


Run
----

This ``plugin`` can be run in two modes: natively as a python package or as a containerized docker image.

Using PyPI
~~~~~~~~~~

To run from PyPI, simply do a 

.. code:: bash

    pip install pacscopy

and run with

.. code:: bash

    pacscopy.py --man /tmp /tmp

to get inline help. To copy from one directory to another, simply do

.. code:: bash

    pacscopy.py --dir /some/input/directory /destination/directory


Using ``docker run``
~~~~~~~~~~~~~~~~~~~~

To run using ``docker``, be sure to assign an "input" directory to ``/incoming`` and an output directory to ``/outgoing``. *Make sure that the* ``$(pwd)/out`` *directory is world writable!*

Now, prefix all calls with 

.. code:: bash

    docker run --rm -v $(pwd)/out:/outgoing                             \
            fnndsc/pl-pacscopy pacscopy.py                              \

Thus, getting inline help is:

.. code:: bash

    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            fnndsc/pl-pacscopy pacscopy.py                              \
            --man                                                       \
            /outgoing

Examples
--------

Copy a directory ``dataset/MPRAGE`` to the output directory. If called from ChRIS, the input directory spec refers to a location in openstorage, otherwise it is interpreted as a system directory spec.

.. code:: bash

    mkdir out
    docker run --rm -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
            fnndsc/pl-pacscopy pacscopy.py                              \
            --dir dataset/MPRAGE                                        \
            /outgoing






