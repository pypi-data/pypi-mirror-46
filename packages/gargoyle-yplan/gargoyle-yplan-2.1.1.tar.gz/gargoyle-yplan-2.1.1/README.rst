========
Gargoyle
========

.. image:: https://img.shields.io/pypi/v/gargoyle-yplan.svg
    :target: https://pypi.python.org/pypi/gargoyle-yplan

.. image:: https://travis-ci.org/adamchainz/gargoyle.svg?branch=master
    :target: https://travis-ci.org/adamchainz/gargoyle

.. image:: https://readthedocs.org/projects/gargoyle-yplan/badge/?version=latest
        :target: https://gargoyle-yplan.readthedocs.io/en/latest/

**Retired: this project is no longer maintained.** I (Adam Johnson) no longer
have time to continue maintaining this. I was doing so since I took on this
project, and its related packages
`django-modeldict <https://github.com/adamchainz/django-modeldict>`__ and
`nexus <https://github.com/adamchainz/nexus>`__, for my ex-employer YPlan. If
you'd like to sponsor ongoing maintenance or take it over yourself, please
contact me@adamj.eu.

Gargoyle is a platform built on top of Django which allows you to switch functionality of your application on and off
based on conditions.

It was originally created by `Disqus <https://github.com/disqus/gargoyle>`_, but due to the inactivity we at YPlan have
taken over maintenance on this fork.

Requirements
------------

Tested with all combinations of:

* Python: 3.6
* Django: 1.11, 2.0, 2.1, 2.2

Python 3.4+ supported.

Install
-------

Install it with **pip**:

.. code-block:: bash

    pip install gargoyle-yplan

If you are upgrading from the original to this fork, you will need to run the following first, since the packages clash:

.. code-block:: bash

    pip uninstall django-modeldict gargoyle

Failing to do this will mean that ``pip uninstall gargoyle`` will also erase the files for ``gargoyle-yplan``, and
similarly for our ``django-modeldict`` fork.

Documentation
-------------

The documentation is available at `Read The Docs <https://gargoyle-yplan.readthedocs.io/>`_.
