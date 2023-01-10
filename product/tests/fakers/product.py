import factory

from product.models import Product


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("name")
    slug = factory.Faker("slug")
    picture = factory.django.ImageField(color="blue")
    brand = factory.SubFactory("product.tests.fakers.brand.BrandFactory")
    category = factory.SubFactory(
        "product.tests.fakers.category.CategoryFactory"
    )
    pet_type = factory.SubFactory(
        "product.tests.fakers.pet_type.PetCategoryFactory"
    )
