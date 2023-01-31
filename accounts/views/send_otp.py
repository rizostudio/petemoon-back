import re

from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from accounts.functions import send_sms_otp
from accounts.models import OneTimePassword, User

phone_number_regex = re.compile(r"^09\d{9}")


class OTPThrottle(AnonRateThrottle):
    scope = "otp"


class SendOTP(APIView):
    permission_classes = []
    # throttle_classes = [OTPThrottle]

    def post(self, *args, **kwargs):
        phone_number = self.request.data.get("phone_number")
        if not phone_number_regex.match(phone_number):
            return Response(
                {"success": False, "errors": [_("invalid phone number")]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if OneTimePassword.otp_exist(phone_number):
            return Response(
                {"success": False, "errors": [_("otp already sent")]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_type = self.request.data.get("user_type", "normal")
        if user_type not in [
            choice[0] for choice in User.user_type_choices[:-1]
        ]:
            user_type = "normal"
        if User.objects.filter(phone_number=phone_number).exists():
            user = User.objects.get(phone_number=phone_number)
            if user.user_type != user_type:
                return Response(
                    {
                        "success": False,
                        "errors": [
                            _("user registered with different user type")
                        ],
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            user = User.objects.create_user(
                phone_number=phone_number, user_type=user_type
            )
        otp = OneTimePassword(user)
        done = send_sms_otp(phone_number, otp.code)
        if not done:
            return Response(
                {"success": False, "errors": [_("error in sending otp")]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "success": True,
                "data": {"otp_id": otp.otp_id},
            },
            status=status.HTTP_200_OK,
        )
