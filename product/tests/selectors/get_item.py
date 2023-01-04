from django.test import TestCase

from product.selectors import get_item_by_slug
from product.tests.fakers import (
    CommentFactory,
    ProductFactory,
    ProductPricingFactory,
)


class GetItemSelectorTestCase(TestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.pricing = ProductPricingFactory(
            product=self.product, price_after_sale=None, inventory=1
        )
        self.lower_pricing = ProductPricingFactory(
            product=self.product,
            price=self.pricing.price + 1,
            price_after_sale=self.pricing.price - 1,
            inventory=1,
        )
        self.unavailable_pricing = ProductPricingFactory(
            product=self.product,
            price=self.lower_pricing.price_after_sale - 10,
            price_after_sale=None,
            inventory=0,
        )
        self.non_related_pricing = ProductPricingFactory(
            price=self.lower_pricing.price_after_sale - 10
        )
        self.comment = CommentFactory(product=self.product)
        self.second_comment = CommentFactory(product=self.product)
        self.unpublished_comment = CommentFactory(
            product=self.product, published=False
        )
        self.unrelated_comment = CommentFactory()

    def test_get_item_by_slug_selector(self):
        product = get_item_by_slug(self.product.slug)
        self.assertEqual(product, self.product)
        self.assertEqual(product.price, self.lower_pricing.price_after_sale)
        self.assertEqual(
            product.rating, (self.comment.rate + self.second_comment.rate) / 2
        )
