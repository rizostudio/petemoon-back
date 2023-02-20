import random

from django.test import LiveServerTestCase
from rest_framework import status
from rest_framework.test import RequestsClient

from accounts.functions import login
from accounts.tests.fakers import UserFactory
from product.models import ProductPricing
from product.tests.fakers import PetshopFactory, ProductFactory


class AddUpdatePricingViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.user = UserFactory(user_type="petshop")
        self.petshop = PetshopFactory(owner=self.user.petshop_profile)
        self.user.petshop_profile.is_approved = True
        self.user.petshop_profile.save()

        self.none_petshop_user = UserFactory(user_type="normal")

        self.rc = RequestsClient()

        self.user_token = login(self.user)[0]
        self.none_petshop_token = login(self.none_petshop_user)[0]

    def make_request(self, slug, token=None, data=None):
        return self.rc.patch(
            f"{self.live_server_url}/product/{slug}/pricing/",
            json=data,
            headers={"Authorization": f"Bearer {token}"},
        )

    def test_403_response(self):
        response = self.make_request(self.product.slug)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.make_request(
            self.product.slug, token=self.none_petshop_token
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_404_response(self):
        response = self.make_request("invalid", token=self.user_token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(
            response.json(),
            {"success": False, "errors": {"message": "Product not found."}},
        )

    def test_400_response(self):
        response = self.make_request(self.product.slug, token=self.user_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                "success": False,
                "errors": {
                    "price": ["This field is required."],
                    "inventory": ["This field is required."],
                },
            },
        )

    def test_200_response(self):
        data = {
            "price": random.randint(1, 100),
            "inventory": random.randint(1, 100),
        }
        response = self.make_request(
            self.product.slug, token=self.user_token, data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(),
            {"success": True, "data": {"message": "Pricing added."}},
        )
        self.assertTrue(
            ProductPricing.objects.filter(
                product=self.product,
                petshop=self.petshop,
                price_after_sale=None,
                **data,
            ).exists()
        )
