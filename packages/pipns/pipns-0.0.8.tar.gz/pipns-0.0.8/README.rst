pipns
=====

|PyPi Version|

**NOTE: This tool is under active development and is broken in many ways.**

Isolated, named Python environments.

* Install packages in isolated pipenv environments.
* Provides common PATH and MANPATH variables to access resources of explicitly installed packages.
* Easily rebuild or update all environments. (Great for Python upgrades).
* Inspired by `pipsi <https://github.com/mitsuhiko/pipsi>`_.


Examples
--------

Usage is basically the same as pipenv with the exception of namespace
specification (``-n`` or ``--all``).

Installing a package
++++++++++++++++++++

.. code:: shell

    $ pipns install zepusu
    $ . ~/.pipns/shell.sh
    $ command -v zepusu
    /home/user/.pipns/bin/zepusu

Updating environments
+++++++++++++++++++++

.. code:: shell

    $ pipns --all update

Listing environments
++++++++++++++++++++

.. code:: shell

    $ pipns --list

Rebuilding environments
+++++++++++++++++++++++

.. code:: shell

    $ pipns --all --rm
    $ pipns --all install


Installation
------------

.. code:: shell

    $ pip install pipns


.. |PyPi Version| image:: https://img.shields.io/pypi/v/pipns.svg?
   :target: https://pypi.python.org/pypi/pipns
