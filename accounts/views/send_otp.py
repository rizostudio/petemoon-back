import re

from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from accounts.functions import send_sms
from accounts.models import OneTimePassword, User

phone_number_regex = re.compile(r"^09\d{9}")


class OTPThrottle(AnonRateThrottle):
    scope = "otp"


class SendOTP(APIView):
    permission_classes = []
    throttle_classes = [OTPThrottle]

    def post(self, *args, **kwargs):
        phone_number = self.request.data.get("phone_number")
        if not phone_number_regex.match(phone_number):
            return Response(
                {"error": _("invalid phone number")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if OneTimePassword.otp_exist(phone_number):
            return Response(
                {"error": _("otp already sent")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if User.objects.filter(phone_number=phone_number).exists():
            user = User.objects.get(phone_number=phone_number)
        else:
            user = User.objects.create_user(phone_number=phone_number)
        otp = OneTimePassword(user)
        done = send_sms(phone_number, otp.code)
        if not done:
            return Response(
                {"error": _("error in sending otp")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"otp_id": otp.otp_id}, status=status.HTTP_200_OK)
