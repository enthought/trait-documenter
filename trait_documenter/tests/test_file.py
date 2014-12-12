from traits.api import Float, HasTraits, Property

module_trait = Float


class Dummy(HasTraits):

    trait_1 = Float

    trait_2 = Property(
        Float,
        depends_on='trait_1')

    not_trait = 2
