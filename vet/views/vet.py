from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import exceptions
from ..serializers import VisitSerializer, VetSingleSerializer
from dashboard.models import Address
from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException
from accounts.views.permissions import IsVet
from accounts.models import VetProfile



class VetListView(APIView):
    serializer_class = VetSingleSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        query_params = self.request.query_params
        if query_params.get("pet_type_experience") != None:
            vet_list = VetProfile.objects.filter(pet_type_experience=query_params.get("pet_type_experience"))
        else:
            vet_list = VetProfile.objects.all()

        order_by = query_params.get("order_by")
        if order_by == "created_at":
            vet_list = vet_list.order_by("created_at")

        result = self.serializer_class(vet_list, many=True).data
        return SuccessResponse(data=result)