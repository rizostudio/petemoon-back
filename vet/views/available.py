from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import exceptions, status
from rest_framework.response import Response
from ..serializers import PotentialTimeSerializer, AvailableTimeSerializer, ReserveTimeSerializer, VetTimesSerializer
from config.exceptions import CustomException
from accounts.views.permissions import IsVet
from accounts.models import VetProfile
from ..models import ReserveTimes, Visit
from django.shortcuts import get_object_or_404
from django.conf import settings
import json
import requests
from config.responses import bad_request, SuccessResponse, UnsuccessfulResponse
from utils.choices import Choices




# tooooodooooooo
class AvailableTimesView(APIView):
    serializer_class = AvailableTimeSerializer
    permission_classes = [IsVet]

    def post(self, request):
        date = request.data['date']
        vet_profile = VetProfile.objects.get(user=request.user)
        #reserved_time = vet_profile.reserve_times.all()
        #date_reserved_time = vet_profile.reserve_times.filter(time__date=date)

        serialized_data = self.serializer_class(data=request.data)
        try:
            serialized_data.is_valid()
            vet_profile = VetProfile.objects.get(user=request.user)
            times = serialized_data.validated_data["available_time"]
            reserved_time = vet_profile.reserve_times.filter(time__date=date)

            for time in times:
                reserve_time = ReserveTimes.objects.create(time=time, vet=vet_profile)
                if reserved_time.filter(time=reserve_time.time).exists():
                    pass
                else:
                    vet_profile.reserve_times.add(reserve_time)

            times_serializer = VetTimesSerializer(reserved_time, many=True)
            return SuccessResponse(data=times_serializer.data)

        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)

