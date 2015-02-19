from traits.api import Float, HasTraits, Property, Range

module_trait = Float

long_module_trait = Range(
    low=0.2,
    high=34)

class Dummy(HasTraits):

    trait_1 = Float

    trait_2 = Property(
        Float,
        depends_on='trait_1')

    not_trait = 2
