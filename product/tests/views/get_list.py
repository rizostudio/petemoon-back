from django.test import LiveServerTestCase
from rest_framework import status
from rest_framework.test import RequestsClient

from product.serializers import ProductListSerializer
from product.tests.fakers import (
    CommentFactory,
    ProductFactory,
    ProductPricingFactory,
)


class GetListViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.pricing = ProductPricingFactory(
            product=self.product, price_after_sale=None, inventory=1
        )
        self.lower_pricing = ProductPricingFactory(
            product=self.product,
            price=self.pricing.price + 1,
            price_after_sale=self.pricing.price - 1,
            inventory=2,
        )
        ProductPricingFactory(
            product=self.product,
            price=self.lower_pricing.price_after_sale - 10,
            price_after_sale=None,
            inventory=0,
        )
        ProductPricingFactory(price=self.lower_pricing.price_after_sale - 10)
        CommentFactory(product=self.product)
        CommentFactory(product=self.product)
        CommentFactory(product=self.product, published=False)
        CommentFactory()
        self.rc = RequestsClient()

    def make_request(self, **kwargs):
        return self.rc.get(f"{self.live_server_url}/product/", params=kwargs)

    def test_200_response(self):
        response = self.make_request(
            pet_types=[self.product.animal_type],
            category_slugs=[self.product.category.slug],
            max_price=self.pricing.price,
            min_price=self.lower_pricing.price_after_sale,
            brand_slugs=[self.product.brand.slug],
            order_by="cheapest",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(),
            {
                "success": True,
                "data": {
                    "products": ProductListSerializer(
                        [self.product], many=True
                    ).data,
                    "count": 1,
                },
            },
        )
