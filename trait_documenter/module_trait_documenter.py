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
from __future__ import unicode_literals

import ast
import inspect
from _ast import Assign

from sphinx.ext.autodoc import (
    ModuleDocumenter, ModuleLevelDocumenter, SUPPRESS)


class ModuleTraitDocumenter(ModuleLevelDocumenter):
    """ Specialised Documenter subclass for module traits.

    The class defines a new documenter that recovers the trait definition
    signature of class level traits.

    """

    objtype = 'traitattribute'
    directivetype = 'attribute'
    member_order = 60

    # must be higher than other attribute documenters
    priority = 12

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        """ Check that the documented member is a trait instance.
        """
        return (
            isattr and
            hasattr(member, 'as_ctrait') and
            not isinstance(parent, ModuleDocumenter))

    def document_members(self, all_members=False):
        # Trait attributes have no members """
        pass

    def import_object(self):
        """ Setup the necessary info for documenting the trait definition.

        Notes
        -----
        Code adapted from autodoc.Documenter.import_object.

        """
        import pdb; pdb.set_trace()
        ModuleLevelDocumenter.import_object(self)

    def add_content(self, more_content, no_docstring=False):
        # Never try to get a docstring from the trait object.
        ModuleLevelDocumenter.add_content(
            self, more_content, no_docstring=True)

    def add_directive_header(self, sig):
        """ Add the sphinx directives.

        Add the 'attribute' directive with the annotation option
        set to the trait definition.

        """
        ModuleLevelDocumenter.add_directive_header(self, sig)
        if not self.options.annotation:
            definition = self.get_trait_definition()
            self.add_line(
                u'   :annotation: = {0}'.format(definition), '<autodoc>')
        elif self.options.annotation is SUPPRESS:
            pass
        else:
            self.add_line(
                u'   :annotation: %s' % self.options.annotation, '<autodoc>')

    def get_trait_definition(self):
        """ Retrieve the Trait attribute definition
        """
        # Get the class source.
        source = inspect.getsource(self.parent)

        # Get the trait definition
        ast_nodes = ast.parse(source)
        for node in ast.iter_child_nodes(ast_nodes):
            if isinstance(node, Assign):
                name = node.targets[0]
                if name.id == self.object_name:
                    break
        else:
            raise RuntimeError('Could not find trait definition')

        endlineno = name.lineno
        for item in ast.walk(node):
            if hasattr(item, 'lineno'):
                endlineno = max(endlineno, item.lineno)

        definition_lines = [
            line.strip()
            for line in source.splitlines()[name.lineno-1:endlineno]]
        definition = ''.join(definition_lines)
        equal = definition.index('=')
        return definition[equal + 1:].lstrip()
