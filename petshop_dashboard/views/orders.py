from django.utils.translation import gettext_lazy as _
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException
from product.models import ProductPricing
from ..serializers import OrdersSerializer
from product.models import Petshop
from shopping_cart.models import Order, PetShopOrder



class OrdersView(APIView):

    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query_params = self.request.query_params
        if query_params['orders_type']=='recent':
            orders = Order.objects.filter(
            products__petshop__owner__user=request.user).distinct().order_by('-created_at')

        if query_params['orders_type']=='completed':

            orders = Order.objects.filter(
                products__petshop__owner__user=request.user,status="DELIVERED").distinct()

        if orders:
            price_count = 0
            for order in orders:
                d = PetShopOrder.objects.filter(user_order=order)
                
                p = d.aggregate(Sum('price'))
                order.total_price = p['price__sum']

                order.product=d
            for product in d:
                price_count += product.price

        result = self.serializer_class(orders, many=True).data
        return SuccessResponse(data=result)

class SingleOrderView(APIView):

    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query_params = self.request.query_params
        if query_params['orders_type']=='recent':
            orders = Order.objects.filter(
            products__petshop__owner__user=request.user).distinct().order_by('-created_at')

        if query_params['orders_type']=='completed':

            orders = Order.objects.filter(
                products__petshop__owner__user=request.user,status="DELIVERED").distinct()

        if orders:
            price_count = 0
            for order in orders:
                d = PetShopOrder.objects.filter(user_order=order)
                
                p = d.aggregate(Sum('price'))
                order.total_price = p['price__sum']

                order.product=d
            for product in d:
                price_count += product.price

        result = self.serializer_class(orders, many=True).data
        return SuccessResponse(data=result)

