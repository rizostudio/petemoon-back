from django.test import LiveServerTestCase
from rest_framework import status
from rest_framework.test import RequestsClient

from accounts.models import OneTimePassword
from accounts.tests.fakers import UserFactory


class VerifyOTPViewTestCase(LiveServerTestCase):
    def setUp(self):
        self.rc = RequestsClient()

    def make_request(self, otp_id, otp):
        return self.rc.post(
            f"{self.live_server_url}/accounts/otp/verify/",
            json={"otp_id": otp_id, "otp_code": otp},
        )

    def test_400_response(self):
        response = self.make_request("invalid", "invalid")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {"error": "OTP is invalid"})

    def test_200_response(self):
        user = UserFactory()
        otp = OneTimePassword(user)
        response = self.make_request(otp.otp_id, otp.code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json().get("is_registered"), user.is_registered
        )
        self.assertIn("refresh_token", response.json())
        self.assertIn("HTTP_ACCESS", response.cookies)
