from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from .serializers import (PetGeneralSerializer,PetMidicalSerializer)
from .models import Pet



class AccountVeiw(APIView):
    pass

class OrdersVeiw(APIView):
    pass

class PetMedicalVeiw(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = PetMidicalSerializer

    def get(self, request):
        try:
            try:
                pet_medical = Pet.objects.get(owner=request.user)
            except Pet.DoesNotExist:
                raise Exception(detail=_("Subject is not registerd yet"))
            result = self.get_serializer().data
            return Response(data=result)
        except Exception as e:
            return Response(error=e.detail, status=e.status_code)
   


class PetGeneralVeiw(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = PetGeneralSerializer

    def get(self, request):
        try:
            try:
                pet_general = Pet.objects.get(owner=request.user)
            except Pet.DoesNotExist:
                raise Exception(detail=_("You don't have any pet"))
            result = self.get_serializer(data=pet_general).data
            return Response(data=result)
        except Exception as e:
            return Response(error=e.detail, status=e.status_code)
   