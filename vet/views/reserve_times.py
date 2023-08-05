from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import exceptions, status
from rest_framework.response import Response
from ..serializers import PotentialTimeSerializer,AvailableTimeSerializer, ReserveTimeSerializer
from dashboard.models import Address
from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException
from accounts.views.permissions import IsVet
from accounts.models import VetProfile
from ..models import ReserveTimes, Visit
from django.shortcuts import get_object_or_404



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
        reserved_time = vet_profile.reserve_times.filter(reserved=False)
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


class AvailableReserveForNormalUserView(APIView):
    serializer_class = AvailableTimeSerializer
    permission_classes = [AllowAny]
    def get(self, *args, **kwargs):
        vet_profile = VetProfile.objects.get(id=kwargs.get("id"))
        reserved_time = vet_profile.reserve_times.filter(reserved=False)
        result = self.serializer_class(reserved_time, many=True).data
        return SuccessResponse(data=result)


class ReserveForNormalUserView(APIView):
    serializer_class = ReserveTimeSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serialized_data = self.serializer_class(data=request.data)
        try:
            serialized_data.is_valid()
            vet_profile = VetProfile.objects.get(id=kwargs.get("id"))
            time = serialized_data.validated_data["time"]
            reserved_time = vet_profile.reserve_times.filter(reserved=False).values_list("time", flat=True)

            #for ReserveTime in reserved_time:
                #print(ReserveTime.strftime("%m/%d/%Y,%H:%M:%S"))

            if time in reserved_time:
                reserve = ReserveTimes.objects.get(vet=vet_profile,time=time)
                #reserve = get_object_or_404(ReserveTimes, time=time)
                reserve.reserved = True
                reserve.save()
                visit = Visit()
                visit.vet = vet_profile.user
                visit.user = request.user
                visit.time = reserve
                visit.status = "Pending"
                visit.save()
                return SuccessResponse(data=time)
            else:
                return Response("The time you enter is already reserved or does not exist in vet's available times.", status=status.HTTP_406_NOT_ACCEPTABLE)

        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)


