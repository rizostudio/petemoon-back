import factory

from dashboard.models import PetCategory, PetType


class PetTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PetType

    pet_type = factory.Faker("name")
    specific_type = factory.Faker("pyint", min_value=1, max_value=3)


class PetCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PetCategory

    pet_category = factory.Faker("name")
    pet_type = factory.SubFactory(PetTypeFactory)
    slug = factory.Faker("slug")
