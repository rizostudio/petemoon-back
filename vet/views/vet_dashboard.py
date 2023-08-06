from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
from ..serializers import PastVisitSerializer,SinglePastVisitSerializer,FutureVisitSerializer, SingleFutureVisitSerializer
from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException
from accounts.views.permissions import IsVet
from ..models import Visit
from django.db.models import Q
from utils.choices import Choices
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from dashboard.serializers import AddressSerializer
from shopping_cart.models import PetShopOrder, Order
from product.models.pricing import ProductPricing



class VetDashboardView(APIView):
    permission_classes = [IsVet]

    def get(self, request):
        income = PetShopOrder.objects.filter(product__petshop__owner__user=request.user).aggregate(Sum('price_with_shipping_and_fee'))
        messages = None
        products_count = ProductPricing.objects.filter(petshop__owner__user=request.user).count()
        orders_count = Order.objects.filter(products__petshop__owner__user=request.user).count()
        order_history = PetShopOrder.objects.filter(product__petshop__owner__user=request.user)

        return SuccessResponse(data={
            "income": income['price_with_shipping_and_fee__sum'],
            "messages": messages,
            "products_count": products_count,
            "orders_count": orders_count,
            "orders_history": PetShopOrdersSerializer(order_history, many=True).data
        })





class PastVisitView(APIView):

    permission_classes = [IsVet]
    serializer_class = PastVisitSerializer

    def get(self, request):
        try:
            visit = Visit.objects.filter(
                Q(vet=request.user) & Q(status=Choices.Visit.CANCELED) | Q(status=Choices.Visit.DONE))
            serialized_data = self.serializer_class(visit, many=True).data
            
            return SuccessResponse(data=serialized_data)
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)


