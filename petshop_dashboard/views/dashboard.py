from django.utils.translation import gettext_lazy as _
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from dashboard.serializers import AddressSerializer
from shopping_cart.models import PetShopOrder,Order
from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException

from product.models.pricing import ProductPricing

from ..serializers.orders import PetShopOrdersSerializer


class DashboardView(APIView):

    #serializer_class = AddressSerializer
    #authentication_classes = []
    permission_classes = [IsAuthenticated]

    def get(self, request):
        income = PetShopOrder.objects.filter(product__petshop__owner__user=request.user).aggregate(Sum('price_with_shipping_and_fee'))
        messages = None
        products_count = ProductPricing.objects.filter(petshop__owner__user=request.user).count()
        orders_count = Order.objects.filter(products__petshop__owner__user=request.user).count()
        order_history = PetShopOrder.objects.filter(product__petshop__owner__user=request.user)

        return SuccessResponse(data={
            "income":income['price_with_shipping_and_fee__sum'],
            "messages":messages,
            "products_count":products_count,
            "orders_count":orders_count,
            "orders_history":PetShopOrdersSerializer(order_history, many=True).data
            
            })


