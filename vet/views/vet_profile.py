from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
from config.responses import SuccessResponse, UnsuccessfulResponse
from dashboard.serializers import UserProfileSerializer
from vet.serializers import VetProfileSerialzer
from dashboard.models import Pet
from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException
from accounts.models import VetProfile


class VetProfileView(APIView):
    serializer_class = VetProfileSerialzer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = VetProfile.objects.get(user=request.user)
        result = VetProfileSerialzer(profile).data
        #result = self.serializer_class(self.request.user,  many=True).data
        return SuccessResponse(data=result)

