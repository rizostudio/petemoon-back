from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException

from .utils import add_to_cart, get_cart
from .serializers import CartSerializer


class CartView(APIView):

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        redis_cart = get_cart(request.user.id)
        for key,value in redis_cart.items():
            pass

        return SuccessResponse(data=redis_cart)

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        try:
            if serialized_data.is_valid(raise_exception=True):
                print(serialized_data.validated_data['product_pricing_id'])
                add_to_cart(
                    request.user.id, serialized_data.validated_data['product_pricing_id'],
                     serialized_data.validated_data['count'])
                return SuccessResponse(data={"message": _("prodct added to your cart successfuly")})
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
