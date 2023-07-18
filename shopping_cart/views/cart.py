from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException

from ..utils import add_to_cart, get_cart
from product.models.pricing import ProductPricing
from ..serializers.cart import CartGetSerializer, CartPostSerializer

from dashboard.models import Address
from dashboard.serializers import AddressSerializer


class CartView(APIView):
    serializer_class = CartGetSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            redis_cart = get_cart(request.user.id)
            print(redis_cart)

            if redis_cart != None:
                products = []
                total_price = 0

                for key, value in redis_cart['products'].items():
                    product_in_cart = ProductPricing.objects.get(id=key)
                    product_in_cart.count = value
                    product_in_cart.products_accumulative_price = product_in_cart.count * \
                        product_in_cart.price
                    total_price += product_in_cart.products_accumulative_price
                    products.append(CartGetSerializer(product_in_cart).data)

                products.append({"total_price": total_price})
            else:
                raise CustomException(detail=_("Shopping cart is empty"))
            address = Address.objects.get(id=redis_cart['address'],user=request.user)
            return SuccessResponse(
                data={"products":products,"address":AddressSerializer(address).data})

        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)


    def post(self, request):
        serialized_data = CartPostSerializer(data=request.data)
        try:
            
            if serialized_data.is_valid(raise_exception=True):
                add_to_cart(request.user.id, dict(serialized_data.validated_data))

                return SuccessResponse(data={"message": _("Cart saved successfuly")})
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
