from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException

from ..utils import get_cart
from product.models.pricing import ProductPricing
from ..serializers import ShippingSerializer
from shopping_cart.models import Shipping


class ShippingView(APIView):
    serializer_class = ShippingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        try:
            shipping = Shipping.objects.all()

            serialized_data = self.serializer_class(shipping,many=True).data
            return SuccessResponse(data=serialized_data)
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)

    