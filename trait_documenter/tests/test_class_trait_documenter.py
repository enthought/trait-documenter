from __future__ import unicode_literals
import unittest

import mock

from trait_documenter.class_trait_documenter import ClassTraitDocumenter
from trait_documenter.tests import test_file
from trait_documenter.tests.test_file import Dummy


class TestClassTraitDocumenter(unittest.TestCase):

    def test_can_document_member(self):
        can_document_member = ClassTraitDocumenter.can_document_member
        parent = mock.Mock()

        # modules
        parent.object = test_file
        self.assertFalse(can_document_member(Dummy, 'Dummy', True, parent))
        self.assertFalse(can_document_member(Dummy, 'Dummy', False, parent))
        self.assertFalse(can_document_member(
            test_file.module_trait, 'module_trait', False, parent))
        self.assertFalse(can_document_member(
            test_file.module_trait, 'module_trait', True, parent))

        # class
        parent.object = Dummy
        self.assertTrue(
            can_document_member(
                Dummy.class_traits()['trait_1'], 'trait_1', True, parent))
        self.assertFalse(
            can_document_member(
                Dummy.class_traits()['trait_1'], 'trait_1', False, parent))
        self.assertFalse(
            can_document_member(
                Dummy.not_trait, 'not_trait', False, parent))

    def test_import_object(self):
        # given
        documenter = ClassTraitDocumenter(mock.Mock(), 'test')
        documenter.modname = u'trait_documenter.tests.test_file'
        documenter.objpath = [u'Dummy', u'trait_1']

        # when
        documenter.import_object()

        # then
        self.assertEqual(documenter.object_name, u'trait_1')
        self.assertTrue(documenter.object is None)
        self.assertEqual(documenter.parent, Dummy)

    def test_add_directive_header(self):
        # given
        documenter = ClassTraitDocumenter(mock.Mock(), u'test')
        documenter.parent = Dummy
        documenter.object_name = u'trait_2'
        documenter.modname = u'trait_documenter.tests.test_file'
        documenter.get_sourcename = mock.Mock(return_value='<autodoc>')
        documenter.objpath = [u'Dummy', u'trait_2']
        documenter.add_line = mock.Mock()

        # when
        documenter.add_directive_header('')

        # then
        expected = [
            (u'.. py:attribute:: Dummy.trait_2', u'<autodoc>'),
            (u'   :noindex:', u'<autodoc>'),
            (u'   :module: trait_documenter.tests.test_file', u'<autodoc>'),
            (u"   :annotation: = Property(Float,depends_on='trait_1')", u'<autodoc>')]  # noqa
        calls = documenter.add_line.call_args_list
        for index, call in enumerate(calls):
            self.assertEqual(tuple(call)[0], expected[index])


if __name__ == '__main__':
    unittest.main()
