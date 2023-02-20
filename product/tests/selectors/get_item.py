from django.test import TestCase

from product.selectors import (
    get_item_by_slug,
    get_item_list,
    get_on_sales,
    get_product_id_by_slug,
)
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

    def test_get_item_list(self):
        products, count = get_item_list(
            pet_types=[self.product.pet_type.slug],
            pet_categories=[self.product.pet_type.pet_type.specific_type],
            category_slugs=[self.product.category.slug],
            max_price=self.pricing.price,
            min_price=self.lower_pricing.price_after_sale,
            brand_slugs=[self.product.brand.slug],
            order_by="cheapest",
        )
        self.assertEqual(count, 1)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0], self.product)

    def test_get_product_id_by_slug(self):
        self.assertEqual(
            self.product.id, get_product_id_by_slug(self.product.slug)
        )

    def test_get_on_sales(self):
        result = get_on_sales(1, 0)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.product)
