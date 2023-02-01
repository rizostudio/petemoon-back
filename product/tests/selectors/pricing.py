import random

from django.test import TestCase

from product.models import ProductPricing
from product.selectors import add_update_pricing
from product.tests.fakers import PetshopFactory, ProductFactory


class PricingSelectorTestCase(TestCase):
    def setUp(self):
        self.petshop = PetshopFactory()
        self.product = ProductFactory()

    def test_add_update_pricing_selector(self):
        inventory = random.randint(1, 100)
        price = random.randint(1, 100)
        add_update_pricing(
            pet_shop_id=self.petshop.id,
            product_id=self.product.id,
            price=price,
            inventory=inventory,
        )
        self.assertTrue(
            ProductPricing.objects.filter(
                product=self.product,
                inventory=inventory,
                price=price,
                petshop=self.petshop,
                price_after_sale=None,
            ).exists()
        )
