from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from ..serializers import PotentialTimeSerializer
from dashboard.models import Address
from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException


class PotentialTimeView(APIView):

    serializer_class = PotentialTimeSerializer
    permission_classes = [IsAuthenticated]



    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        try:
            serialized_data.is_valid()
            time = serialized_data.validated_data.get("time")

            date_list = []
            from datetime import datetime, timedelta
            for i in range(36):
                time = time + timedelta(minutes=30)
                date_list.append(time)
            return SuccessResponse(data=date_list)

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