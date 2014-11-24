"""
    A Trait Documenter
    (Subclassed from the autodoc ClassLevelDocumenter)

    :copyright: Copyright 2014 by Enthought, Inc

"""
import ast
import traceback
import sys
import inspect
from _ast import ClassDef, Assign

from traits.trait_handlers import TraitType
from traits.has_traits import MetaHasTraits
from sphinx.ext.autodoc import ClassLevelDocumenter


def is_class_trait(name, cls):
    """ Check if the name is in the list of class defined traits of ``cls``.
    """
    return isinstance(cls, MetaHasTraits) and name in cls.__class_traits__


class TraitDocumenter(ClassLevelDocumenter):
    """ Specialized Documenter subclass for trait attributes.

    The class defines a new documenter that recovers the trait definition
    signature of module level and class level traits.

    To use the documenter, append the module path in the extension
    attribute of the `conf.py`.

    .. warning::

        Using the TraitDocumenter in conjunction with TraitsDoc is not
        advised.

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
            issubclass(type(member), TraitType) or
            is_class_trait(membername, parent.object))

    def document_members(self, all_members=False):
        # Trait attributes have no members """
        pass

    def add_content(self, more_content, no_docstring=False):
        # Never try to get a docstring from the trait object.
        ClassLevelDocumenter.add_content(
            self, more_content, no_docstring=True)

    def import_object(self):
        """ Get the Trait object.

        Notes
        -----
        Code adapted from autodoc.Documenter.import_object.

        """
        try:
            __import__(self.modname)
            current = self.module = sys.modules[self.modname]
            for part in self.objpath[:-1]:
                current = self.get_attr(current, part)
            name = self.objpath[-1]
            self.object_name = name
            self.object = None
            self.parent = current
            return True
        # this used to only catch SyntaxError, ImportError and
        # AttributeError, but importing modules with side effects can raise
        # all kinds of errors.
        except Exception, err:
            if self.env.app and not self.env.app.quiet:
                self.env.app.info(traceback.format_exc().rstrip())
            msg = (
                'autodoc can\'t import/find {0} {r1}, it reported error: '
                '"{2}", please check your spelling and sys.path')
            self.directive.warn(msg.format(
                self.objtype, str(self.fullname), err))
            self.env.note_reread()
            return False

    def add_directive_header(self, sig):
        """ Add the sphinx directives.

        Add the 'attribute' directive with the annotation option
        set to the trait definition.

        """
        ClassLevelDocumenter.add_directive_header(self, sig)
        definition = self.get_trait_definition()
        self.add_line(
            u'   :annotation: = {0}'.format(definition), '<autodoc>')

    def get_trait_definition(self):
        """ Retrieve the Trait attribute definition
        """
        # Get the class source and tokenize it.
        source = inspect.getsource(self.parent)

        nodes = ast.parse(source)
        for node in ast.iter_child_nodes(nodes):
            if isinstance(node, ClassDef):
                parent_node = node
                break
        else:
            return ''

        for node in ast.iter_child_nodes(parent_node):
            if isinstance(node, Assign):
                name = node.targets[0]
                if name.id == self.object_name:
                    break
        else:
            return ''

        endlineno = name.lineno
        for item in ast.walk(node):
            if hasattr(item, 'lineno'):
                endlineno = max(endlineno, item.lineno)

        definition_lines = [
            line.strip()
            for line in source.splitlines()[name.lineno-1:endlineno]]
        definition = ''.join(definition_lines)
        equal = definition.index(u'=')
        return definition[equal + 1:].lstrip()
