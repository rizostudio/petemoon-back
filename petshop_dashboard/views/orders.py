from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
from config.responses import SuccessResponse
from ..serializers import OrdersSerializer, UserDetailsSerializer, OrderSingleSerializer
from shopping_cart.models import Order, PetShopOrder
from accounts.models import PetshopProfile
from product.models import Petshop, ProductPricing
from product.serializers import ProductPricingSerializer
from payment.models import PetshopSaleFee


class OrdersView(APIView):
    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query_params = self.request.query_params
        if query_params['orders_type'] == 'recent':
            orders = Order.objects.filter(
                products__petshop__owner__user=request.user).distinct().order_by('-created_at')

        if query_params['orders_type'] == 'completed':
            orders = Order.objects.filter(
                products__petshop__owner__user=request.user, status="DELIVERED").distinct()

        if orders:
            price_count = 0
            for order in orders:
                d = PetShopOrder.objects.filter(user_order=order)

                p = d.aggregate(Sum('price'))
                order.total_price = p['price__sum']

                order.product = d
            for product in d:
                price_count += product.price

        result = self.serializer_class(orders, many=True).data
        return SuccessResponse(data=result)



class SingleOrderView(APIView):

    serializer_class = OrdersSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        order = Order.objects.get(id=id)

        product_pricing_ids = []
        petshops = PetShopOrder.objects.filter(user_order=order)
        for petshop in petshops:
            products = ProductPricing.objects.filter(id=petshop.product.id)
            for product in products:
                if product.petshop == Petshop.objects.get(owner=PetshopProfile.objects.get(user=request.user)):
                    product_pricing_ids.append(product.id)
        product_pricings = ProductPricing.objects.filter(id__in=product_pricing_ids)


        price_count = 0
        for product in product_pricings:
            price_count += product.price

        shipping = order.shipping_method.price
        fee = PetshopSaleFee.objects.all().first().percent
        total = (price_count-((price_count*fee)/100))+shipping,

        finance = {'price': price_count, 'shiping': shipping, 'fee':str(fee)+"%", 'total':total }


        return SuccessResponse(
            data={"order": OrderSingleSerializer(order).data,
                  "products": ProductPricingSerializer(product_pricings, many=True).data,
                  "user": UserDetailsSerializer(order).data,
                  "finance": finance})
