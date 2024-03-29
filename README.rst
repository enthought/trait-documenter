Trait-Documenter
================

.. image:: https://travis-ci.org/enthought/trait-documenter.svg?branch=master
   :target: https://travis-ci.org/enthought/trait-documenter

.. image:: http://codecov.io/github/enthought/trait-documenter/coverage.svg?branch=master
   :target: http://codecov.io/github/enthought/trait-documenter?branch=master

.. image:: https://readthedocs.org/projects/trait-documenter/badge/?version=latest
   :target: https://readthedocs.org/projects/trait-documenter/?badge=master


Trait-Documenter is an autodoc extension to allow trait definitions to be
properly rendered in sphinx.

Project Status
--------------

This project is a work in progress. For production use, use the existing
``traits.util.trait_documenter`` Sphinx extension (which is distributed
as part of Traits) instead.

Installation
------------

Development versions can be found at https://github.com/enthought/trait-documenter.

The package requires a recent version of  *sphinx*, *traits* and *astor* to function properly.

Usage
-----

Add the trait-documenter to the extensions variable in your *conf.py*::

  extensions.append('trait_documenter')

.. warning::

  Using the TraitDocumenter in conjunction with the TraitsDoc package
  is not advised.


Example
-------

A class trait with a docstring::

   from traits.api import HasTraits, Float

   class MyClass(HasTraits):

       #: A float number.
       number = Float(2.0)


Will be rendered as::

   .. py:attribute:: number
      :annotation: = Float(2.0)

      A float number.
