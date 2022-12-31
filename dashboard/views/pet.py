from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from config.responses import SuccessResponse, UnsuccessfulResponse
from dashboard.serializers import PetGeneralSerializer, PetMidicalSerializer
from dashboard.models import Pet
from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException


class PetGeneralView(APIView):
    serializer_class = PetGeneralSerializer
    authentication_classes = []
    permission_classes = [IsAuthenticated]

    def get(self, request):
           
        pet_general = Pet.objects.filter(owner=request.user)
        result = self.get_serializer(pet_general).data
        return SuccessResponse(data=result)

    def patch(self, request, id=None):
        serialized_data = self.serializer_class(request.user,data=request.data, partial=True)

        try:
            if serialized_data.is_valid(raise_exception=True):

                pet = Pet.objects.get(id=id)

                serialized_data.update(instance=pet,validated_data=serialized_data.validated_data)

                return SuccessResponse(
                    message=_("Pet updated successfuly"))

        except CustomException as e:
            return UnsuccessfulResponse(error=e.detail, status=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(error=e.detail, status=e.status_code)


    
        
