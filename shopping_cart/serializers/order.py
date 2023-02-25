from rest_framework import serializers
from dashboard.serializers import AddressSerializer
from product.serializers.pricing import ProductPricingSerializer
from shopping_cart.models import Order,PetShopOrder
from dashboard.models import Address
from ..utils import order_completion
from django.db import transaction
#from shopping_cart.serializers  import ShippingSerializer
from .. models import Shipping


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

        for product in products:
            PetShopOrder.objects.create(user_order=order,price=product.price,product=product)
            order.products.add(product)

        order.save()


        order_completion(validated_data['total_price'], validated_data['user'])

        return order
