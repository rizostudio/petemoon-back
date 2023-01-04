from django.test import LiveServerTestCase
from rest_framework import status
from rest_framework.test import RequestsClient

from product.serializers import ProductGetSerializer
from product.tests.fakers import (
    CommentFactory,
    ProductFactory,
    ProductPricingFactory,
)


class GetItemViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.product = ProductFactory()
        pricing = ProductPricingFactory(
            product=self.product, price_after_sale=None, inventory=1
        )
        lower_pricing = ProductPricingFactory(
            product=self.product,
            price=pricing.price + 1,
            price_after_sale=pricing.price - 1,
            inventory=1,
        )
        # unavailable_pricing
        ProductPricingFactory(
            product=self.product,
            price=lower_pricing.price_after_sale - 10,
            price_after_sale=None,
            inventory=0,
        )
        # non_related_pricing
        ProductPricingFactory(price=lower_pricing.price_after_sale - 10)
        # comment
        CommentFactory(product=self.product)
        # second_comment
        CommentFactory(product=self.product)
        # unpublished_comment
        CommentFactory(product=self.product, published=False)
        # unrelated_comment
        CommentFactory()
        self.rc = RequestsClient()

    def make_request(self, slug):
        return self.rc.get(f"{self.live_server_url}/product/{slug}/")

    def test_404_response(self):
        response = self.make_request("invalid")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(
            response.json(),
            {"success": False, "errors": ["Item not found."]},
        )

    def test_200_response(self):
        response = self.make_request(self.product.slug)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(),
            {
                "success": True,
                "data": ProductGetSerializer(self.product).data,
            },
        )
