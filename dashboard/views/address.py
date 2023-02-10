from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from dashboard.serializers import AddressSerializer
from dashboard.models import Address
from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException


class AddressView(APIView):

    serializer_class = AddressSerializer
    #authentication_classes = []
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:

            address = Address.objects.get(id=id,user=request.user)
            result = self.serializer_class(address).data

        else:
            address = Address.objects.filter(user=request.user)
            result = self.serializer_class(address,many=True).data

        return SuccessResponse(data=result)


    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        try:
            if serialized_data.is_valid(raise_exception=True):
                serialized_data.save(user=request.user)
                return SuccessResponse(data={"message":_("Address added successfuly")})
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)


    def patch(self, request, id=None):
        serialized_data = self.serializer_class(request.user,data=request.data, partial=True)

        try:
            if serialized_data.is_valid(raise_exception=True):

                address = Address.objects.filter(id=id)

                serialized_data.update(instance=address,validated_data=serialized_data.validated_data)

                return SuccessResponse(data={"message":_("Address updated successfuly")})

        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)


    def delete(self, request, id=None):
        try:
            try:
                address = Address.objects.get(id=id).delete()
            except Address.DoesNotExist:
                raise CustomException(detail=_("address does not exist"))

            return SuccessResponse(data={"message":_("Address deleted successfuly")})
                
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)       