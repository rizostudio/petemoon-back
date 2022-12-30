from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from config.responses import SuccessResponse, UnsuccessfulResponse
from dashboard.serializers import PetSerializer
from dashboard.models import Pet
from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException


class PetGeneralView(APIView):
    serializer_class = PetSerializer
    #authentication_classes = []
    permission_classes = [IsAuthenticated]

    def get(self, request):
           
        pet_general = Pet.objects.filter(user=request.user)
        result = self.serializer_class(pet_general,many=True).data
        return SuccessResponse(data=result)

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        try:
            if serialized_data.is_valid(raise_exception=True):
                serialized_data.save(user=request.user)
                return SuccessResponse(data={"message":_("Pet added successfuly")})
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)


    def patch(self, request, id=None):
        serialized_data = self.serializer_class(request.user,data=request.data, partial=True)

        try:
            if serialized_data.is_valid(raise_exception=True):

                pet = Pet.objects.filter(id=id)

                serialized_data.update(instance=pet,validated_data=serialized_data.validated_data)

                return SuccessResponse(data={"message":_("Pet updated successfuly")})

        except CustomException as e:
            return UnsuccessfulResponse(error=e.detail, status=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(error=e.detail, status=e.status_code)     
