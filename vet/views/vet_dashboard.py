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
from django.db.models import Sum
from dashboard.models import Message
from accounts.serializers import UserSerializer, VetRegisterSerializer
from accounts.models import VetProfile
from vet.models import Visit



class VetDashboardView(APIView):
    permission_classes = [IsVet]

    def get(self, request):
        income = Visit.objects.filter(vet=request.user).aggregate(Sum('price'))
        messages = Message.objects.filter(user=request.user)
        vet = VetProfile.objects.get(user=request.user)
        visits_count = Visit.objects.filter(vet=request.user).count()

        return SuccessResponse(data={
            "income": income['price__sum'],
            "messages": messages,
            "messages_count": messages.count(),
            "visits_count": visits_count,
            "user_data": UserSerializer(request.user).data,
            "vet_data": VetRegisterSerializer(vet).data
        })




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

