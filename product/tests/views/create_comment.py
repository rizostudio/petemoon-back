from django.test import LiveServerTestCase
from rest_framework import status
from rest_framework.test import RequestsClient

from accounts.functions import login
from accounts.tests.fakers import UserFactory
from product.models import Comment
from product.serializers import CommentCreateSerialzer
from product.tests.fakers import ProductFactory


class CreateCommentViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.product = ProductFactory()
        self.user = UserFactory()
        self.rc = RequestsClient()
        self.access_token, _ = login(self.user)

    def make_request(self, slug, data=None, headers=None):
        return self.rc.post(
            f"{self.live_server_url}/product/{slug}/",
            json=data,
            headers=headers,
        )

    def test_403_response(self):
        response = self.make_request(slug=self.product.slug)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_404_response(self):
        response = self.make_request(
            slug="invalid",
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(
            response.json(),
            {"success": False, "errors": ["Product not found."]},
        )

    def test_400_response(self):
        response = self.make_request(
            slug=self.product.slug,
            data={},
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(),
            {
                "success": False,
                "errors": {
                    "title": ["This field is required."],
                    "text": ["This field is required."],
                    "rate": ["This field is required."],
                },
            },
        )

    def test_201_response(self):
        data = {"title": "title", "text": "text", "rate": 2}
        response = self.make_request(
            slug=self.product.slug,
            data=data,
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Comment.objects.filter(
                product=self.product, user=self.user, **data
            ).exists()
        )
        self.assertDictEqual(
            response.json(),
            {
                "success": True,
                "data": CommentCreateSerialzer(
                    Comment.objects.get(
                        product=self.product, user=self.user, **data
                    )
                ).data,
            },
        )
