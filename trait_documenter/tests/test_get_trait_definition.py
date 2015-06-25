from __future__ import unicode_literals
import unittest

from trait_documenter.tests import test_file, test_file2
from trait_documenter.tests.test_file import Dummy
from trait_documenter.util import get_trait_definition


class TestGetTraitDefinition(unittest.TestCase):

    def test_get_simple_module_trait_definition(self):
        # given
        parent = test_file
        object_name = 'module_trait'

        # when
        definition = get_trait_definition(parent, object_name)

        # then
        self.assertEqual(definition, 'Float')

    def test_get_multi_line_module_trait_definition(self):
        # given
        parent = test_file
        object_name = 'long_module_trait'

        # when
        definition = get_trait_definition(parent, object_name)

        # then
        self.assertEqual(definition, "Range(low=0.2,high=34)")

    def test_get_simple_class_trait_definition(self):
        # given
        parent = Dummy
        object_name = 'trait_1'

        # when
        definition = get_trait_definition(parent, object_name)

        # then
        self.assertEqual(definition, 'Float')

    def test_get_multi_line_class_trait_definition(self):
        # given
        parent = Dummy
        object_name = 'trait_2'

        # when
        definition = get_trait_definition(parent, object_name)

        # then
        self.assertEqual(definition, "Property(Float,depends_on='trait_1')")

    def test_get_trait_definition_over_horrible_assigment(self):
        # given
        parent = test_file2
        object_name = 'trait_1'

        # when
        definition = get_trait_definition(parent, object_name)

        # then
        self.assertEqual(definition, "Event")

    def test_get_trait_definition_inside_if_block(self):
        # given
        parent = test_file2
        object_name = 'trait_2'

        # when
        definition = get_trait_definition(parent, object_name)

        # then
        self.assertEqual(definition, "List(Int)")


if __name__ == '__main__':
    unittest.main()
