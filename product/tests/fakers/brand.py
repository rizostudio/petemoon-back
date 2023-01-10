import factory

from product.models import Brand


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Faker("name")
    slug = factory.Faker("slug")
