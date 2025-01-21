from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework.views import APIView
from rest_framework import exceptions
from accounts.functions import (
    apply_stage,
    check_petshop_register_stage,
    get_user_data,
)
from accounts.models import VetProfile
from accounts.views.permissions import IsVet
from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException
from ..serializers import VetRegisterSerializer
from rest_framework import status
from django.conf import settings

class VetRegisterView(APIView):
    permission_classes = [IsVet]
    serializer_class =  VetRegisterSerializer

    def get(self, request):
        order = VetProfile.objects.filter(user=request.user)
        result = self.serializer_class(order,many=True).data
        return SuccessResponse(data=result)


    def patch(self, request):
        serialized_data = self.serializer_class(request.user,data=request.data, partial=True)
        try:
            if serialized_data.is_valid(raise_exception=True):

                try:
                    if serialized_data.validated_data['national_card_front'].size > settings.MAX_UPLOAD_SIZE:
                        return UnsuccessfulResponse(errors="You cannot upload national_card_front file more than 5Mb",status_code=status.HTTP_406_NOT_ACCEPTABLE)
                except:
                    pass

                try:
                    if serialized_data.validated_data['national_card_back'].size > settings.MAX_UPLOAD_SIZE:
                        return UnsuccessfulResponse(errors="You cannot upload national_card_back file more than 5Mb",status_code=status.HTTP_406_NOT_ACCEPTABLE)
                except:
                    pass

                try:
                    if serialized_data.validated_data['birth_certificate'].size > settings.MAX_UPLOAD_SIZE:
                        return UnsuccessfulResponse(errors="You cannot upload birth_certificate file more than 5Mb", status_code=status.HTTP_406_NOT_ACCEPTABLE)
                except:
                    pass

                try:
                    if serialized_data.validated_data['medical_card'].size > settings.MAX_UPLOAD_SIZE:
                        return UnsuccessfulResponse(errors="You cannot upload medical_card file more than 5Mb",status_code=status.HTTP_406_NOT_ACCEPTABLE)
                except:
                    pass

                try:
                    if serialized_data.validated_data['military_card'].size > settings.MAX_UPLOAD_SIZE:
                        return UnsuccessfulResponse(errors="You cannot upload military_card file more than 5Mb",status_code=status.HTTP_406_NOT_ACCEPTABLE)
                except:
                    pass

                vet_profile = serialized_data.update(
                    instance=VetProfile.objects.filter(
                    user=request.user),validated_data=serialized_data.validated_data)
                user = request.user
                user.register_completed = True
                user.first_name = request.data['first_name']
                user.last_name = request.data['last_name']
                user.save()
                vet = VetProfile.objects.get(user=request.user)
                vet.first_name = request.data['first_name']
                vet.last_name = request.data['last_name']
                vet.save()
                return SuccessResponse(data=self.serializer_class(vet_profile,many=True).data)

        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)     

