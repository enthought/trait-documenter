from __future__ import unicode_literals
import unittest

import mock

from trait_documenter.trait_documenter import (
    is_class_trait, TraitDocumenter)
from trait_documenter.tests import test_file
from trait_documenter.tests.test_file import Dummy


class TestTraitDocumenter(unittest.TestCase):

    def test_is_class_trait(self):
        self.assertTrue(is_class_trait('trait_1', Dummy))
        self.assertTrue(is_class_trait('trait_2', Dummy))
        self.assertFalse(is_class_trait('not_trait', Dummy))
        self.assertFalse(is_class_trait('__dict__', object))
        self.assertFalse(is_class_trait('__dict__', object))

    def test_can_document_member(self):
        can_document_member = TraitDocumenter.can_document_member
        parent = mock.Mock()

        # modules
        parent.object = test_file
        self.assertFalse(can_document_member(Dummy, 'Dummy', True, parent))
        self.assertFalse(can_document_member(Dummy, 'Dummy', True, parent))

        parent.object = Dummy
        self.assertTrue(
            can_document_member(
                Dummy.class_traits()['trait_1'], 'trait_1', True, parent))
        self.assertTrue(
            can_document_member(
                Dummy.class_traits()['trait_1'], 'trait_1', False, parent))

    def test_get_simple_trait_definition(self):
        documenter = TraitDocumenter(mock.Mock(), 'test')
        documenter.parent = Dummy
        documenter.object_name = 'trait_1'
        definition = documenter.get_trait_definition()
        self.assertEqual(definition, 'Float')

    def test_get_multi_line_trait_definition(self):
        documenter = TraitDocumenter(mock.Mock(), 'test')
        documenter.parent = Dummy
        documenter.object_name = 'trait_2'
        definition = documenter.get_trait_definition()
        self.assertEqual(definition, "Property(Float,depends_on='trait_1')")

    def test_module_level_trait_definition(self):
        documenter = TraitDocumenter(mock.Mock(), 'test')
        documenter.parent = test_file
        documenter.object_name = 'trait_2'
        definition = documenter.get_trait_definition()
        self.assertEqual(definition, "Property(Float,depends_on='trait_1')")


if __name__ == '__main__':
    unittest.main()
