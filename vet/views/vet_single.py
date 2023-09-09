from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import exceptions

from ..serializers import PotentialTimeSerializer,AvailableTimeSerializer, VetSingleSerializer
from dashboard.models import Address
from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException
from accounts.views.permissions import IsVet

from accounts.models import VetProfile
from ..models import ReserveTimes


class VetSingleView(APIView):
    permission_classes = [AllowAny]
    serializer_class = VetSingleSerializer
    def get(self, *args, **kwargs):
        try:
            vet = VetProfile.objects.get(id=kwargs.get("id"))
            serialized_data = self.serializer_class(vet).data
            return SuccessResponse(data=serialized_data)
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)




class AvailableReserveTimeView(APIView):

    serializer_class = AvailableTimeSerializer
    permission_classes = [IsVet]

    def get(self, request):
        vet_profile = VetProfile.objects.get(user=request.user)
        reserved_time = vet_profile.reserve_times.filter(reserved=False)
        result = self.serializer_class(reserved_time,many=True).data
        return SuccessResponse(data=result)

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        try:
            serialized_data.is_valid()
            vet_profile = VetProfile.objects.get(user=request.user)

            #times = serialized_data.validated_data["time"]
            times = request.data['time']
            reserved_time = vet_profile.reserve_times.all()
            
            for time in times:
                    reserve_time = ReserveTimes.objects.create(time=time, vet=VetProfile.objects.get(user=request.user))
                    if reserved_time.filter(time=reserve_time.time).exists():
                        pass
                    else:
                        vet_profile.reserve_times.add(reserve_time)
            return SuccessResponse(data=times)

        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)



