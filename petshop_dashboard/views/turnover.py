from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException
from product.models import Petshop
from product.models.pricing import ProductPricing
from shopping_cart.models import Order, PetShopOrder
from django.db.models import Sum

class TurnOverView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):       
        start_date =  self.request.query_params.get("start_date")
        end_date =  self.request.query_params.get("end_date")   
       
        total_income  = PetShopOrder.objects.filter(
            product__petshop__owner__user=request.user,created_at__range=(start_date, end_date)).aggregate(Sum('price'))
        orders_count = Order.objects.filter(
            products__petshop__owner__user=request.user,created_at__range=(start_date, end_date)).count()
        if total_income['price__sum'] != None:

            profit = total_income['price__sum']-((20*total_income['price__sum'])/100)

        return SuccessResponse(data={
            "total_incom":total_income['price__sum'],
            "orders_count":orders_count,
            "profit":profit,
            "settlement date":None,
            "status":None
            
            })

    