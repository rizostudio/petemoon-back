from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from ..serializers import VisitSerializer
from dashboard.models import Address
from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException
from accounts.views.permissions import IsVet

from accounts.models import VetProfile

from ..models import ReserveTimes


class VisitView(APIView):

    permission_classes = [IsVet]
    serializer_class = VisitSerializer

    # def get(self, request, id=None):
    #     try:
            
    #         vet = VetProfile.objects.get(user=request.user)
    #         serialized_data = self.serializer_class(vet).data
            
    #         return SuccessResponse(data=serialized_data)
    #     except CustomException as e:
    #         return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)


    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        try:
            if serialized_data.is_valid(raise_exception=True):
                serialized_data.save(user=request.user)
            return SuccessResponse(data={"message":_("Visit added successfuly")})

        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        
     