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
        parent = ModuleDocumenter(mock.Mock(), 'test')

        # modules
        parent.object = test_file
        self.assertFalse(can_document_member(Dummy, 'Dummy', True, parent))
        self.assertFalse(can_document_member(Dummy, 'Dummy', False, parent))
        self.assertFalse(can_document_member(
            test_file.module_trait, 'module_trait', False, parent))
        self.assertTrue(can_document_member(
            test_file.module_trait, 'module_trait', True, parent))

        # class
        parent.object = Dummy
        self.assertFalse(
            can_document_member(
                Dummy.class_traits()['trait_1'], 'trait_1', True, parent))
        self.assertFalse(
            can_document_member(
                Dummy.class_traits()['trait_1'], 'trait_1', False, parent))

    def test_import_object(self):
        # given
        documenter = ModuleTraitDocumenter(mock.Mock(), 'test')
        value = mock.Mock(return_value=[])
        documenter.env.config.autodoc_mock_imports = value
        documenter.modname = u'trait_documenter.tests.test_file'
        documenter.objpath = [u'long_module_trait']

        # when
        documenter.import_object()

        # then
        self.assertEqual(documenter.object_name, u'long_module_trait')
        self.assertIsNone(documenter.object)
        self.assertEqual(documenter.parent, test_file)

    def test_add_directive_header(self):
        # given
        documenter = ModuleTraitDocumenter(mock.Mock(), '_test')
        documenter.parent = Dummy
        documenter.object_name = 'trait_2'
        documenter.modname = u'trait_documenter._tests._test_file'
        documenter.objpath = [u'Dummy', u'trait_2']
        documenter.add_line = mock.Mock()

        # when
        documenter.add_directive_header('')

        # then
        expected = [
            (u'.. py:attribute:: Dummy.trait_2', u'<autodoc>'),
            (u'   :noindex:', u'<autodoc>'),
            (u'   :module: trait_documenter._tests._test_file', u'<autodoc>'),
            (u"   :annotation: = Property(Float,depends_on='trait_1')", u'<autodoc>')]  # noqa
        calls = documenter.add_line.call_args_list
        for index, call in enumerate(calls):
            self.assertSequenceEqual(tuple(call)[0], expected[index])


if __name__ == '__main__':
    unittest.main()
