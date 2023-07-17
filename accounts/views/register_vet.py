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

                vet_profile = serialized_data.update(
                    instance=VetProfile.objects.filter(
                    user=request.user),validated_data=serialized_data.validated_data)
                return SuccessResponse(data=self.serializer_class(vet_profile,many=True).data)

        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)     

