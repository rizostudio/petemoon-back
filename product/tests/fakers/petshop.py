import factory

from product.models import Petshop


class PetshopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Petshop

    name = factory.Faker("name")
    slug = factory.Faker("slug")
