from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.functions import get_user_data, login
from accounts.models import OneTimePassword
from accounts.selectors import get_user
from config.settings import ACCESS_TTL
from ..functions import validate_token
from config.responses import SuccessResponse, UnsuccessfulResponse


class UserValidationView(APIView):
    #authentication_classes = []
    #permission_classes = [IsAuthenticated]

    def post(self, request):
           
        data = request.data
        is_valid = validate_token(data['access_token'])
        return SuccessResponse(data={"is_valid":is_valid})

   