robot-framework-percy
=====================

.. contents::

Introduction
------------
Robot framework client library for visual regression testing with Percy.

Installation
------------

The recommended installation method is using pip::

.. code:: bash

    pip install robot-framework-percy

Usage
-----

.. code:: robotframework

    Open browser              url              Chrome
    Percy Initialize Build
    Percy Snapshot            snapshot name
    Percy Finalize Build

