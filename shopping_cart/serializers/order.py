from rest_framework import serializers
from dashboard.serializers import AddressSerializer
from product.serializers.pricing import ProductPricingSerializer
from shopping_cart.models import Order
from dashboard.models import Address
from ..utils import order_completion
from django.db import transaction


class OrderGetSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order_id = serializers.CharField()
    status = serializers.CharField()
    address = AddressSerializer()
    products = ProductPricingSerializer(many=True)
    total_price = serializers.IntegerField()


class OrderPostSerializer(serializers.Serializer):
    address = serializers.IntegerField()
    shipping_method = serializers.CharField()

    @transaction.atomic
    def create(self, validated_data):
        address = validated_data.pop("address")
        address = Address.objects.get(id=address)
        products = validated_data.pop("products")
        order = Order(**validated_data)
        order.address = address
        order.save()
        for product in products:
            order.products.add(product)

        order_completion(validated_data['total_price'], validated_data['user'])

        return order
