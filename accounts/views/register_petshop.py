from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework import status
from accounts.functions import (
    apply_stage,
    check_petshop_register_stage,
    get_user_data,
)
from accounts.models import PetshopProfile
from accounts.views.permissions import IsPetShop
from config.responses import bad_request, ok
from ..serializers import PetShopRegisterSerializer

from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException
from django.conf import settings



class RegisterPetshop(APIView):
    permission_classes = [IsPetShop]
    serializer_class =  PetShopRegisterSerializer

    def get(self, request):
           
        order = PetshopProfile.objects.filter(user=request.user)
        result = self.serializer_class(order,many=True).data
        return SuccessResponse(data=result)


    def patch(self, request):
        serialized_data = self.serializer_class(request.user,data=request.data, partial=True)
        user = self.request.user
        try:
            if serialized_data.is_valid(raise_exception=True):

                try:
                    if serialized_data.validated_data['national_card'].size > settings.MAX_UPLOAD_SIZE:
                        return UnsuccessfulResponse(errors="You cannot upload file more than 5Mb",status_code=status.HTTP_406_NOT_ACCEPTABLE)
                except:
                    pass

                petshop = serialized_data.update(
                    instance=PetshopProfile.objects.filter(
                    user=request.user),validated_data=serialized_data.validated_data)
                user.register_completed = True
                user.first_name = serialized_data.validated_data['first_name']
                user.last_name = serialized_data.validated_data['last_name']
                user.save()
                petshop_profile = PetshopProfile.objects.get(user=user)
                petshop_profile.first_name = serialized_data.validated_data['first_name']
                petshop_profile.last_name = serialized_data.validated_data['last_name']
                petshop_profile.save()
                return SuccessResponse(data=self.serializer_class(petshop,many=True).data)

        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)     
