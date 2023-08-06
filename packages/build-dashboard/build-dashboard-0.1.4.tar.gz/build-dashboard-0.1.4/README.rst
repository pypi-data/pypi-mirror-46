build-dashboard: A CLI dashboard for Buildbot
==================================================

.. image:: https://travis-ci.org/ReverentEngineer/build-dashboard.svg?branch=master
    :target: https://travis-ci.org/ReverentEngineer/build-dashboard

:Site:  https://github.com/ReverentEngineer/build-dashboard
:Original author: Jeff Hill <jeff@reverentengineer.com>


.. contents::
   :local:

build-dashboard is an open-source client for Buildbot that allows for reviewing builds in the terminal.


Requirements
------------

Required packages include: aiohttp, toml, asciimatics

How to run
-------------

.. code-block:: bash

    build_dashboard  --protocol https --host buildbot.example.com

Configuration file
-------------------

build_dashboard looks for a TOML-based `.buildbotrc` in the users home directory. If it finds one it, it will use the parameters in the file. Any arguments passed on the command line will override the configuration file.

Example configuration file:

.. code-block:: ini

    protocol = "http"
    host = "localhost"
    unix = "/var/run/buildbot.sock"
