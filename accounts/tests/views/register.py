import faker
from django.test import LiveServerTestCase
from rest_framework import status
from rest_framework.test import RequestsClient

from accounts.functions import login
from accounts.tests.fakers import UserFactory


class RegisterViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.client = RequestsClient()
        self.user = UserFactory(first_name="", last_name="")
        self.access, _ = login(self.user)
        self.registered_user = UserFactory()
        self.registered_access, _ = login(self.registered_user)
        self.faker = faker.Faker()

    def make_request(self, data=None, access=None):
        return self.client.patch(
            f"{self.live_server_url}/accounts/register/",
            json=data,
            headers={"ACCESS": f"Bearer {access}"},
        )

    def test_403_response(self):
        response = self.make_request()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_400_response(self):
        response = self.make_request(
            data={"first_name": "John", "last_name": "Doe"},
            access=self.registered_access,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.json()["success"])
        self.assertListEqual(
            response.json()["errors"], ["user is already registered"]
        )
        response = self.make_request(
            data={
                "email": "invalid_email",
                "first_name": "John",
                "last_name": "Doe",
            },
            access=self.access,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.json()["success"])
        self.assertEqual(response.json()["errors"][0], "incorrect data")
        self.assertIn("email", response.json()["errors"][1])

    def test_200_response(self):
        data = {
            "email": self.faker.email(),
            "first_name": self.faker.first_name(),
            "last_name": self.faker.last_name(),
            "referal_code": "123456",
        }
        response = self.make_request(
            data=data,
            access=self.access,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()["success"])
        self.assertDictEqual(
            response.json()["data"], {"message": "registeration completed"}
        )
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_registered)
        self.assertEqual(self.user.email, data["email"])
        self.assertEqual(self.user.first_name, data["first_name"])
        self.assertEqual(self.user.last_name, data["last_name"])
        self.assertEqual(self.user.profile.referal_code, data["referal_code"])
