import factory

from product.models import ProductPricing


class ProductPricingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductPricing

    price = factory.Faker("pyint", min_value=0, max_value=1000)
    product = factory.SubFactory("product.tests.fakers.product.ProductFactory")
    petshop = factory.SubFactory("product.tests.fakers.petshop.PetshopFactory")
    inventory = factory.Faker("pyint", min_value=0, max_value=1000)
