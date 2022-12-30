from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from dashboard.serializers import OrderSerializer
from dashboard.models import Order
from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException


class OrdersView(APIView):
    serializer_class = OrderSerializer
    #authentication_classes = []
    permission_classes = [IsAuthenticated]

    def get(self, request):
           
        order = Order.objects.filter(user=request.user)
        result = self.serializer_class(order,many=True).data
        return SuccessResponse(data=result)

