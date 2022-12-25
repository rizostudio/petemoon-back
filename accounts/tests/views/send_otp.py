from unittest.mock import patch

import faker
from django.test import LiveServerTestCase
from rest_framework import status
from rest_framework.test import RequestsClient

from accounts.models import OneTimePassword, User
from accounts.tests.fakers import UserFactory


class SendOTPViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.rc = RequestsClient()
        self.faker = faker.Faker()

    def make_request(self, phone_number):
        return self.rc.post(
            f"{self.live_server_url}/accounts/otp/",
            json={"phone_number": phone_number},
        )

    def test_400_response(self):
        response = self.make_request("invalid")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error": "invalid phone number"}
        )
        user = UserFactory()
        OneTimePassword(user)
        response = self.make_request(user.phone_number)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {"error": "otp already sent"})
        user = UserFactory()
        with patch("accounts.views.send_otp.send_sms", new=lambda *_: False):
            response = self.make_request(user.phone_number)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(
            response.json(), {"error": "error in sending otp"}
        )

    def test_200_response(self):
        phone_number = self.faker.numerify("09#########")
        with patch("accounts.views.send_otp.send_sms", new=lambda *_: True):
            response = self.make_request(phone_number)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(OneTimePassword.otp_exist(phone_number))
        self.assertTrue(
            User.objects.filter(phone_number=phone_number).exists()
        )
        self.assertIn("otp_id", response.json())
