from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from ..serializers import PotentialTimeSerializer
from dashboard.models import Address
from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException
from accounts.views.permissions import IsVet

from accounts.models import VetProfile


class PotentialTimeView(APIView):

    serializer_class = PotentialTimeSerializer
    permission_classes = [IsVet]



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




class AvailableReserveTimeView(APIView):

    serializer_class = PotentialTimeSerializer
    permission_classes = [IsVet]



    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        try:
            serialized_data.is_valid()
            vet_profile = VetProfile.objects.get(user=request.user)
            times = serialized_data.validated_data.get("time")
            reserved_time = vet_profile.reserve_times
            
            for time in times:
                if time in reserved_time:
                    pass
                else:
                    vet_profile.reserve_times.add(time)
            

            return SuccessResponse(data=times)

        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)




       