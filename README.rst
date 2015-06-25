Trait-Documenter
================

.. image:: https://travis-ci.org/enthought/trait-documenter.svg?branch=master
    :target: https://travis-ci.org/enthought/trait-documenter

.. image:: http://codecov.io/github/enthought/trait-documenter/coverage.svg?branch=master
    :target: http://codecov.io/github/enthought/trait-documenter?branch=master

Trait-Documenter is an autodoc extension to allow trait definitions to be
properly rendered in sphinx.

Installation
============

The package requires *sphinx* and *traits* to function properly.

Usage
=====

Add the trait-documenter to the extensions variable in your *conf.py*::

  extensions.append('trait_documenter')

.. warning::

  Using the TraitDocumenter in conjunction with the TraitsDoc package
  is not advised.
