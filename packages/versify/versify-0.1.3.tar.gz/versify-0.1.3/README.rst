python-versify : client to the Bible api platforms python friendly
==================================================================

python-versify is a pure python library wich can find many verses on the
bible. The lib relies on Dbt.io for get contents.

|Build Status|

Look how python-versify is usefull

.. code:: python

   from versify.util.Dbt import Dbt

   dbt = Dbt(config_path="/path/to/config.ini")

   # DBY is the code of Darby
   print(dbt.find_verse("DBY", "1 Timothée", 2, 1))

Features support
----------------

-  Find any verse on the bible
-  Find random verse on the bible

Installation
------------

To install python-versify, simple use pip like that:

.. code:: bash

   pip install python-versify

You need a config file for Dbt like :

.. code:: ini

   [dbt]
   key = yourDbtKey
   lang = FRN

Documentation
-------------

Complete documentation is available on `this link`_

How to Contribute
-----------------

1. Check for open issues or open a fresh issue to start a discussion
   around a feature idea or a bug.
2. Fork the repository on GitHub to start making your changes to the
   master branch (or branch off of it).
3. Send a pull request and bug the maintainer until it gets merged and
   published. :) Make sure to add yourself to AUTHORS.

.. _this link: https://python-versify.readthedocs.io/en/latest/index.html

.. |Build Status| image:: https://travis-ci.org/willinprogress/python-versify.svg?branch=master
   :target: https://travis-ci.org/willinprogress/python-versify