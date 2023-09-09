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
from vet.models import Visit
from rest_framework import viewsets, status
from rest_framework.response import Response

class VisitView(APIView):
    permission_classes = [IsVet]
    serializer_class = VisitSerializer

    def post(self, request):
        data=request.data
        data['user']=request.user.id
        serialized_data = self.serializer_class(data=data)
        try:
            if serialized_data.is_valid():
                serialized_data.save()
            return SuccessResponse(data={"message":_("Visit added successfuly")})

        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)


class SingleVisitView(APIView):
    permission_classes = [IsVet]
    serializer_class = VisitSerializer

    def patch(self, request, id=None):
        visit = Visit.objects.get(id=id)
        serialized_data = self.serializer_class(visit,data=request.data, partial=True)
        try:
            if serialized_data.is_valid(raise_exception=True):
                visit_data = serialized_data.update(instance=visit,validated_data=serialized_data.validated_data)
                return Response('Visit updated.', status=status.HTTP_200_OK)
                #return SuccessResponse(data=VisitSerializer(visit).data)

        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)


#  Not applied at the moment