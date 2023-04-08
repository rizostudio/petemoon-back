from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from config.responses import SuccessResponse, UnsuccessfulResponse
from dashboard.serializers import PetGetSerializer, PetPostSerializer, PetTypeSerializer, PetCategorySerializer
from dashboard.models import Pet, PetType, PetCategory
from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException


class PetView(APIView):
    #authentication_classes = []
    permission_classes = [IsAuthenticated]

    def get(self, request):
           
        pet_general = Pet.objects.filter(user=request.user)
        result = PetGetSerializer(pet_general,many=True).data
        return SuccessResponse(data=result)

    def post(self, request):
        serialized_data = PetPostSerializer(data=request.data)
        try:
            if serialized_data.is_valid(raise_exception=True):
                serialized_data.save(user=request.user)
                return SuccessResponse(data={"message":_("Pet added successfuly")})
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)


    def patch(self, request, id=None):
        serialized_data = PetPostSerializer(request.user,data=request.data, partial=True)

        try:
            if serialized_data.is_valid(raise_exception=True):

                pet = Pet.objects.filter(id=id)

                serialized_data.update(instance=pet,validated_data=serialized_data.validated_data)

                return SuccessResponse(data={"message":_("Pet updated successfuly")})

        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)   
          
    def delete(self, request, id=None):
        try:
            try:
                address = Pet.objects.get(id=id).delete()
            except Pet.DoesNotExist:
                raise CustomException(detail=_("Pet does not exist"))

            return SuccessResponse(data={"message":_("Pet deleted successfuly")})
                
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code) 


class SinglePetView(APIView):
    #authentication_classes = []
    serializer_class = PetGetSerializer

    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
           
        pet_general = Pet.objects.get(user=request.user,id=id)
        result = self.serializer_class(pet_general).data
        return SuccessResponse(data=result)

    

class PetTypeView(APIView):
    serializer_class = PetTypeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
           
        pet_type = PetType.objects.all()
        result = self.serializer_class(pet_type,many=True).data
        return SuccessResponse(data=result)
    

class PetCategoryView(APIView):
    serializer_class = PetCategorySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        pet_type = PetType.objects.get(id=id)
        pet_category = PetCategory.objects.filter(pet_type=pet_type)
        result = self.serializer_class(pet_category,many=True).data
        return SuccessResponse(data=result)
    
    