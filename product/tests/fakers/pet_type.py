import factory

from dashboard.models import PetCategory, PetType


class PetTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PetType

    pet_type = factory.Faker("name")


class PetCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PetCategory

    pet_category = factory.Faker("name")
    pet_type = factory.SubFactory(PetTypeFactory)
