from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException

from ..utils import get_cart
from product.models.pricing import ProductPricing
from ..serializers import OrderGetSerializer, OrderPostSerializer
from shopping_cart.models import Order, Shipping

from dashboard.models import Address

class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        try:
            try:
                order = Order.objects.get(id=id, user=request.user)
            except:
                raise CustomException(detail=_("Order does not exist"))

            serialized_data = OrderGetSerializer(order).data
            return SuccessResponse(data=serialized_data)
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)

    def post(self, request):
        # add method post to total price
        serialized_data = OrderPostSerializer(data=request.data)
        try:
            if serialized_data.is_valid(raise_exception=True):
                cart = get_cart(request.user.id)
                if cart == None:
                    raise CustomException(
                        detail=_("Your shopping cart is empty"))

                try:
                    shipping_method = Shipping.objects.get(id=request.data['shipping_method'])
                except Shipping.DoesNotExist:
                    raise CustomException(detail=_("Shipping matching does not exist"))


                try:
                    address = Address.objects.get(id=cart['address'],user=request.user)
                except Address.DoesNotExist:
                    raise CustomException(detail=_("Address matching does not exist"))

                else:
                    products = []
                    total_price = 0
                    for key, value in cart['products'].items():
                        product_in_cart = ProductPricing.objects.get(id=key)
                        products.append(product_in_cart)
                        product_in_cart.count = value
                        product_in_cart.products_accumulative_price = product_in_cart.count * \
                            product_in_cart.price
                        total_price += product_in_cart.products_accumulative_price


                tran = serialized_data.save(user=request.user, total_price=total_price, products=products, address=address)
                return SuccessResponse(data={"data": tran})
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
