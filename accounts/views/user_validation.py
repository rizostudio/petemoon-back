from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.functions import get_user_data, login
from accounts.models import OneTimePassword
from accounts.selectors import get_user
from config.settings import ACCESS_TTL
from ..functions import validate_token
from config import responses


class UserValidationView(APIView):

    def post(self, request):
        user = request.user
        if user.register_completed == False:
            return responses.forbidden(errors={"User has not yet completed registration"})
        if user.user_typer == 'petshop' and user.register_completed == True and user.petshop_profile.is_approved == False:
            return responses.forbidden(errors={"Petshop user has not been approved yet!"})
        cookie = request.COOKIES.get('HTTP_ACCESS')
        if cookie is None:
            return responses.bad_request(errors={"User is not logged in"})
        access_token = cookie.split(' ')[1]
        if validate_token(access_token):
            return responses.ok(data={"is_valid": "True"})
        else:
            return responses.unauthorized(errors={"is_valid": "False"})