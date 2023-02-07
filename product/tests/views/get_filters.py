from django.test import LiveServerTestCase
from rest_framework import status
from rest_framework.test import RequestsClient

from product.tests.fakers import ProductFactory, ProductPricingFactory


class GetFiltersViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.product = ProductFactory()
        pricing_1 = ProductPricingFactory(product=self.product, inventory=1)
        pricing_2 = ProductPricingFactory(product=self.product, inventory=1)
        self.min_price = min(pricing_1.price, pricing_2.price)
        self.max_price = max(pricing_1.price, pricing_2.price)
        self.rc = RequestsClient()

    def test_200_response(self):
        response = self.rc.get(f"{self.live_server_url}/product/filters/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_data = {
            "brands": [
                {
                    "name": self.product.brand.name,
                    "slug": self.product.brand.slug,
                }
            ],
            "categories": [
                {
                    "name": self.product.category.name,
                    "slug": self.product.category.slug,
                }
            ],
            "pet_types": [
                {
                    "name": self.product.pet_type.pet_category,
                    "slug": self.product.pet_type.slug,
                }
            ],
            "pet_categories": [
                {
                    "id": 1,
                    "name": "Dog",
                },
                {
                    "id": 2,
                    "name": "Cat",
                },
                {
                    "id": 3,
                    "name": "Bird",
                },
            ],
            "max_price": self.max_price,
            "min_price": self.min_price,
        }
        self.assertDictEqual(
            response.json(), {"success": True, "data": expected_data}
        )
