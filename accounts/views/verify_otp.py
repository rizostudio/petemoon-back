from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from config import responses

from accounts.functions import get_user_data, login
from accounts.models import OneTimePassword
from accounts.selectors import get_user
from config.settings import ACCESS_TTL
from dashboard.models.wallet import Wallet

from accounts.serializers import UserSerializer



class VerifyOTP(APIView):
    permission_classes = []

    def post(self, *args, **kwargs):
        otp_id = self.request.data.get("otp_id", "")
        otp_code = self.request.data.get("otp_code", "")
        try:
            user_id = OneTimePassword.verify_otp(otp_id, otp_code)
        except ValueError:
            return Response(
                {"success": False, "errors": [_("OTP is invalid")]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = get_user(id=user_id) # self.request.user #

        if user.user_type == 'petshop' and user.register_completed == True and user.petshop_profile.is_approved == False:
            return responses.forbidden(errors={"Petshop user has not been approved yet!"})

        if user.user_type == 'vet' and user.register_completed == True and user.vet_profile.is_approved == False:
            return responses.forbidden(errors={"Vet user has not been approved yet!"})

        access, refresh = login(user)
        try:
            wallet = Wallet.objects.get(user=user)
            credit = wallet.credit
        except:
            credit = None

        data = {
            "refresh_token": refresh,
            "is_registered": user.register_completed,
            "user_type": user.user_type,
            "user_data": UserSerializer(user).data,
            "wallet":credit
        }
        if user.register_completed:
            data["user_data"] = UserSerializer(user).data #get_user_data(user)
        response = Response(
            {
                "success": True,
                "data": data,
            },
            status=status.HTTP_200_OK,
        )
        print('----------------------access-----')
        print(access)
        print('---------------------------------')
        response.set_cookie(
            "HTTP_ACCESS",
            f"Bearer {access}",
            max_age=ACCESS_TTL * 24 * 3600,
            secure=True,
            httponly=True,
            samesite="None",
        )
        return response


