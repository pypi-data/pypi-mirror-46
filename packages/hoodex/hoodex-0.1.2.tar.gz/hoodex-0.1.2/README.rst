======
hoodex
======


.. image:: https://img.shields.io/pypi/v/hoodex.svg
        :target: https://pypi.python.org/pypi/hoodex

.. image:: https://img.shields.io/travis/Ratxi/hoodex.svg
        :target: https://travis-ci.org/Ratxi/hoodex

.. image:: https://readthedocs.org/projects/hoodex/badge/?version=latest
        :target: https://hoodex.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Hoodex checks your plex instance and get the url of the latest uploaded content


* Free software: Apache Software License 2.0
* Documentation: https://hoodex.readthedocs.io.

Install
-------

Install using pip from pypi:

.. code-block:: sh

  pip install hoodex

Usage
-----

You can set your variables via argument when running hoodex or via config file.

With Arguments:

.. code-block:: sh

  hoodex --user my_user --password my_password --server my_server --libraries Movies,TV

With a config file:

.. code-block:: sh

  hoodex --config config.ini

Config
------

You can create a ini config file with the following content:

.. code-block:: ini

  [hoodex]
  PlexUserName = your_user
  PlexPassword = your_password
  PlexServer = your_server
  PlexLibraries = Movies,TV


Features
--------

- Connect to your Plex Server and get the last added elements of a list of libraries

