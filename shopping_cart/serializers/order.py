from rest_framework import serializers
from dashboard.serializers import AddressSerializer
from product.serializers.pricing import ProductPricingSerializer
from shopping_cart.models import Order, PetShopOrder
from dashboard.models import Address
from ..utils import order_completion
from django.db import transaction
#from shopping_cart.serializers  import ShippingSerializer
from .. models import Shipping
from payment.services.create_transaction import create_transaction3


class OrderGetSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order_id = serializers.CharField()
    status = serializers.CharField()
    address = AddressSerializer()
    products = ProductPricingSerializer(many=True)
    total_price = serializers.IntegerField()
    shipping_method = "ShippingSerializer()"


class OrderPostSerializer(serializers.Serializer):
    address = serializers.IntegerField()
    shipping_method = serializers.CharField()

    @transaction.atomic
    def create(self, validated_data):
        address = validated_data.pop("address")
        address = Address.objects.get(id=address)
        products = validated_data.pop("products")
        shipping = validated_data.pop("shipping_method")
        shipping_method = Shipping.objects.get(id=shipping)
        order = Order.objects.create(**validated_data)

        order.address = address
        order.shipping_method = shipping_method
        order.total_price += shipping_method.price
        
        for product in products:
            PetShopOrder.objects.create(
                user_order=order, price=product.price, product=product)
            order.products.add(product)

        order.save()

        tran = create_transaction3(
            user=validated_data.get("user"), 
            amount=order.total_price,
            order=order, transaction_type="order",
            description="some descriptoin")
        print(tran)
        return tran
