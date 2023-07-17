from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from ..serializers import PastVisitSerializer,SinglePastVisitSerializer,FutureVisitSerializer, SingleFutureVisitSerializer
from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException
from accounts.views.permissions import IsVet
from ..models import Visit
from django.db.models import Q

from utils.choices import Choices


class PastVisitView(APIView):

    permission_classes = [IsVet]
    serializer_class = PastVisitSerializer

    def get(self, request):
        try:
            visit = Visit.objects.filter(
                Q(vet=request.user) & Q(status=Choices.Visit.CANCELED) | Q(status=Choices.Visit.DONE))
            serialized_data = self.serializer_class(visit, many=True).data
            
            return SuccessResponse(data=serialized_data)
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)


class SinglePastVisitView(APIView):

    permission_classes = [IsVet]
    serializer_class = SinglePastVisitSerializer

    def get(self, request, id=None):
        try:
            
            visit = Visit.objects.get(vet=request.user,id=id)
            serialized_data = self.serializer_class(visit).data
            
            return SuccessResponse(data=serialized_data)
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)


class FutureVisitView(APIView):

    permission_classes = [IsVet]
    serializer_class = FutureVisitSerializer

    def get(self, request):
        try:
            
            visit = Visit.objects.filter(
                Q(vet=request.user) & Q(status=Choices.Visit.PENDING))
            serialized_data = self.serializer_class(visit, many=True).data
            
            return SuccessResponse(data=serialized_data)
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)


class SingleFutureVisitView(APIView):

    permission_classes = [IsVet]
    serializer_class = SingleFutureVisitSerializer

    def get(self, request, id=None):
        try:
            
            visit = Visit.objects.get(vet=request.user,id=id)
            serialized_data = self.serializer_class(visit).data
            
            return SuccessResponse(data=serialized_data)
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)