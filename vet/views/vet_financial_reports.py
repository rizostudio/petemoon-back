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


class VetFinancialReportsView(APIView):
    permission_classes = [IsVet]

    def get(self, request):
        if self.request.query_params.get("start_date"):
            start_date = self.request.query_params.get("start_date")
        else:
            start_date = '2000-02-22T06:00:00.000Z'

        if self.request.query_params.get("end_date"):
            end_date = self.request.query_params.get("end_date")
        else:
            end_date = '3000-02-22T06:00:00.000Z'

        income = Visit.objects.filter(vet=request.user, created_at__range=(start_date, end_date)).aggregate(Sum('price'))
        visits = Visit.objects.filter(vet=request.user, created_at__range=(start_date, end_date))
        visits_count = visits.count()

        return SuccessResponse(data={
            "total_income": income['price__sum'],
            "visits_count": visits_count,
            "visit": PastVisitSerializer(visits, many=True).data
        })


