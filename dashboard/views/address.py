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
    authentication_classes = []
    permission_classes = [IsAuthenticated]

    def get(self, request):
        address = Address.objects.filter(user=request.user)
        result = self.get_serializer(address).data
        return SuccessResponse(data=result)


    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        try:
            if serialized_data.is_valid(raise_exception=True):
                serialized_data.save()
                return SuccessResponse(message=_("Address added successfuly"))
        except CustomException as e:
            return UnsuccessfulResponse(error=e.detail, status=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(error=e.detail, status=e.status_code)


    def patch(self, request, id=None):
        serialized_data = self.serializer_class(request.user,data=request.data, partial=True)

        try:
            if serialized_data.is_valid(raise_exception=True):

                address = Address.objects.get(id=id)

                serialized_data.update(instance=address,validated_data=serialized_data.validated_data)

                return SuccessResponse(
                    message=_("address updated successfuly")).send()

        except CustomException as e:
            return UnsuccessfulResponse(error=e.detail, status=e.status_code).send()
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(error=e.detail, status=e.status_code).send()

    def delete(self, request, id=None):
        
            address = Address.objects.delete(id=id)

            return SuccessResponse(
                message=_("address deleted successfuly"))

        