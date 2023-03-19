from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from ..serializers import PotentialTimeSerializer,AvailableTimeSerializer
from dashboard.models import Address
from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException
from accounts.views.permissions import IsVet

from accounts.models import VetProfile

from ..models import ReserveTimes

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

    serializer_class = AvailableTimeSerializer
    permission_classes = [IsVet]


    def get(self, request):
           
        vet_profile = VetProfile.objects.get(user=request.user)
        reserved_time = vet_profile.reserve_times.all()
        result = self.serializer_class(reserved_time,many=True).data
        return SuccessResponse(data=result)

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        try:
            serialized_data.is_valid()
            vet_profile = VetProfile.objects.get(user=request.user)
            times = serialized_data.validated_data["available_time"]
            reserved_time = vet_profile.reserve_times.all()
            
            for time in times:
                    reserve_time = ReserveTimes.objects.create(time=time)
                    if reserved_time.filter(time=reserve_time.time).exists():
                        pass
                    else:
                        vet_profile.reserve_times.add(reserve_time)
            
            return SuccessResponse(data=times)

        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)




       