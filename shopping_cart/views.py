from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException

from .utils import add_to_cart, get_cart
from product.models.pricing import ProductPricing
from .serializers import ProductInCartSerializer

class CartView(APIView):

    serializer_class = ProductInCartSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            redis_cart = get_cart(request.user.id)
            if redis_cart != None:
                products = []
                total_price = 0
                for key,value in redis_cart.items():
                    product_in_cart = ProductPricing.objects.get(id=key)
                    product_in_cart.count = value
                    product_in_cart.products_accumulative_price = product_in_cart.count * product_in_cart.price 
                    total_price += product_in_cart.products_accumulative_price
                    products.append(ProductInCartSerializer(product_in_cart).data)
                products.append({"total_price":total_price})
            else:
                raise CustomException(detail=_("Shopping cart is empty"))
            return SuccessResponse(data=products)

        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)


    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        try:
            if serialized_data.is_valid(raise_exception=True):
                print(serialized_data.validated_data['id'])
                add_to_cart(
                    request.user.id, serialized_data.validated_data['id'],
                     serialized_data.validated_data['count'])
                return SuccessResponse(data={"message": _("prodct added to your cart successfuly")})
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
