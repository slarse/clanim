clanim - Command Line Animations
*******************************************************

`Docs`_

.. image:: https://travis-ci.org/slarse/clanim.svg?branch=master
    :target: https://travis-ci.org/slarse/clanim
    :alt: Build Status
.. image:: https://codecov.io/gh/slarse/clanim/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/slarse/clanim
    :alt: Code Coverage
.. image:: https://readthedocs.org/projects/clanim/badge/?version=latest
    :target: http://clanim.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://badge.fury.io/py/clanim.svg
    :target: https://badge.fury.io/py/clanim
    :alt: PyPi Version
.. image:: https://img.shields.io/badge/python-3.6-blue.svg
    :target: https://badge.fury.io/py/pdfebc
    :alt: Supported Python Versions

.. contents::

Overview
========
This package contains decorators for printing a command line animation while
the decorated function runs. It is very similar to the ``decorating`` package,
which currently has way more features and probably serves you better then
``clanim``. I wanted to create ``clanim`` anyway as a means of practicing
with decorators and command line animations. It doesn't seem like ``decorating`` 
currently supports async functions, so that's the one area where ``clanim`` 
potentially is superior at this time.

Requirements
============
Python 3.6 or higher and the ``daiquiri`` package (used for development and
will probably be removed in a final release).

Quickstart
==========
The API for ``clanim`` consists of the ``@animate`` decorator, as well as the
animations in ``clanim.animation``. All of these are package level imports,
so e.g. the ``@animate`` decorator can be accessed like this:

.. code:: python

    # option 1
    import clanim

    @clanim.animate
    def func():
        time.sleep(2)

    # option 2
    from clanim import animate

    @animate
    def func():
        time.sleep(2)

The ``animate`` decorator works both with and without parameters, and supports
both regular functions:

.. image:: images/clanim_sync.gif
    :alt: animate decorator with regular functions

and async functions:

.. image:: images/clanim_async.gif
    :alt: animate decorator with async functions

Install
=======
Option 1: Install from PyPi with ``pip``
----------------------------------------
The latest release of ``clanim`` is on PyPi, and can thus be installed as usual
with ``pip``.  I strongly discourage system-wide ``pip`` installs (i.e. ``sudo
pip install <package>``), as this may land you with incompatible packages in a
very short amount of time. A per-user install can be done like this:

1. Execute ``pip install --user clanim`` to install the package.
2. Further steps to be added ...


Option 2: Clone the repo and the install with ``pip``
-----------------------------------------------------
If you want the dev version, you will need to clone the repo, as only release
versions are uploaded to PyPi. Unless you are planning to work on this
yourself, I suggest going with the release version.

1. Clone the repo with ``git``:
    - ``git clone https://github.com/slarse/clanim``
2. ``cd`` into the project root directory and install with ``pip``.
    - ``pip install --user .``, this will create a local install for the current user.
    - Or just ``pip install .`` if you use ``virtualenv``.
    - For development, use ``pip install -e .`` in a ``virtualenv``.
3. Further steps to be added ...

License
=======
This software is licensed under the MIT License. See the `license file`_ file
for specifics.

Contributing
============
I will happily take contributions, especially in terms of new animations.
Submit a pull request if you have an idea, and let me approve the idea before
you start working on something I would not like in the project!

.. _license file: LICENSE
.. _setup.py: setup.py
.. _requirements.txt: requirements.txt
.. _Docs: https://clanim.readthedocs.io/en/latest/
