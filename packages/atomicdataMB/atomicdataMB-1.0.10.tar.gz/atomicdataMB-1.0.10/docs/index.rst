************
atomicdataMB
************

atomicdataMB provides support for the Neutral Cloud and Exospheres Model
(nexoclom) and can be used as a standalone package.

.. toctree::
  :maxdepth: 2

  atomicmass
  g_values
  photolossrates
  initialize_atomicdata
  LICENSE


Installation
============

Basic installation method:

>>> pip install atomicdataMB

* Requirements

  * python >= 3.6
  * A postgreSQL database server.

  * psycopg2
  * pandas
  * `periodictable <https://periodictable.readthedocs.io/en/latest/index.html>`_

PostgreSQL can be installed using conda:

>>> conda install postgresql

PostgreSQL is also installed when creating the nexoclom python environment
(see XXX).

User Documentation
==================
Explain how to use your software


Reporting Issues
================
How and where should users report problems


Contributing
============
Discuss how or if your software accepts contributions.
This package template has a default CONTRIBUTING.md file
that can be referenced here. It may include sections such as:

* How to make a code contribution
* Coding Guidelines


Reference API
=============
Package documentation usually pulled from docstrings inside the code
