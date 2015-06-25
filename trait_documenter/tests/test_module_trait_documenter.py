from __future__ import unicode_literals
import unittest

import mock
from sphinx.ext.autodoc import ModuleDocumenter

from trait_documenter.module_trait_documenter import ModuleTraitDocumenter
from trait_documenter.tests import test_file
from trait_documenter.tests.test_file import Dummy


class TestModuleTraitDocumenter(unittest.TestCase):

    def test_can_document_member(self):
        can_document_member = ModuleTraitDocumenter.can_document_member
        parent = ModuleDocumenter(mock.Mock(), u'test')

        # modules
        parent.object = test_file
        self.assertFalse(can_document_member(Dummy, u'Dummy', True, parent))
        self.assertFalse(can_document_member(Dummy, u'Dummy', False, parent))
        self.assertFalse(can_document_member(
            test_file.module_trait, u'module_trait', False, parent))
        self.assertTrue(can_document_member(
            test_file.module_trait, u'module_trait', True, parent))

        # class
        parent.object = Dummy
        self.assertFalse(
            can_document_member(
                Dummy.class_traits()[u'trait_1'], u'trait_1', False, parent))

    def test_import_object(self):
        # given
        documenter = ModuleTraitDocumenter(mock.Mock(), u'test')
        documenter.modname = u'trait_documenter.tests.test_file'
        documenter.objpath = [u'long_module_trait']

        # when
        documenter.import_object()

        # then
        self.assertEqual(documenter.object_name, u'long_module_trait')
        self.assertTrue(documenter.object is not None)
        self.assertEqual(documenter.parent, test_file)

    def test_add_directive_header(self):
        # given
        documenter = ModuleTraitDocumenter(mock.Mock(), u'test')
        documenter.parent = test_file
        documenter.options = mock.Mock(annotation=False)
        documenter.modname = u'trait_documenter.tests.test_file'
        documenter.object_name = u'long_module_trait'
        documenter.objpath = [u'long_module_trait']
        documenter.add_line = mock.Mock()

        # when
        documenter.add_directive_header('')

        # then
        expected = [
            (u'.. py:data:: long_module_trait', u'<autodoc>'),
            (u'   :noindex:', u'<autodoc>'),
            (u'   :module: trait_documenter.tests.test_file', u'<autodoc>'),
            (u'   :annotation: = Range(low=0.2,high=34)', u'<autodoc>')]  # noqa
        calls = documenter.add_line.call_args_list
        for index, call in enumerate(calls):
            self.assertEqual(tuple(call)[0], expected[index])


if __name__ == '__main__':
    unittest.main()
