#----------------------------------------------------------------------------
#
#  Copyright (c) 2014, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in /LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
#----------------------------------------------------------------------------
from __future__ import absolute_import


def setup(app):
    """ Add the TraitDocumenter in the current sphinx autodoc instance.

    """
    from trait_documenter.trait_documenter import TraitDocumenter
    app.add_autodocumenter(TraitDocumenter)