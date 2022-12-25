from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.functions import login
from accounts.models import OneTimePassword
from accounts.selectors import get_user
from config.settings import ACCESS_TTL


class VerifyOTP(APIView):
    permission_classes = []

    def post(self, *args, **kwargs):
        otp_id = self.request.data.get("otp_id", "")
        otp_code = self.request.data.get("otp_code", "")
        try:
            user_id = OneTimePassword.verify_otp(otp_id, otp_code)
        except ValueError:
            return Response(
                {"error": _("OTP is invalid")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = get_user(id=user_id)
        access, refresh = login(user)
        response = Response(
            {"refresh_token": refresh, "is_registered": user.is_registered},
            status=status.HTTP_200_OK,
        )
        response.set_cookie(
            "HTTP_ACCESS",
            f"Bearer {access}",
            max_age=ACCESS_TTL,
            httponly=True,
            samesite="Lax",
        )
        return response
