from rest_framework import serializers
from dashboard.serializers import AddressSerializer
from product.serializers.pricing import ProductPricingSerializer
from shopping_cart.models import Order, PetShopOrder
from dashboard.models import Address
from ..utils import order_completion
from django.db import transaction
from .. models import Shipping
from payment.services.create_transaction import create_transaction
from utils.choices import Choices
from payment.models import Discount
from ..utils import random_N_chars_str
from config.exceptions import CustomException


class OrderGetSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order_id = serializers.CharField()
    status = serializers.CharField()
    address = AddressSerializer()
    products = ProductPricingSerializer(many=True)
    total_price = serializers.IntegerField()
    shipping_method = "ShippingSerializer()"
    total_price_with_shipping = serializers.IntegerField()
    


class OrderPostSerializer(serializers.Serializer):
    shipping_method = serializers.CharField()
    discount = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    @transaction.atomic
    def create(self, validated_data):
        discount = validated_data.pop("discount")
        if discount is None:
            discount_percentage = 0
        else:
            try:
                discount = Discount.objects.get(code=discount)
                discount_percentage = discount.percentage
            except Discount.DoesNotExist:
                raise CustomException(detail=("discount matching does not exist"))

        products = validated_data.pop("products")
        shipping_id = validated_data.pop("shipping_method")
        shipping = Shipping.objects.get(id=shipping_id)


        order = Order.objects.create(
            discount=discount,
            address=validated_data.pop("address"),
            shipping_method=shipping,
            **validated_data,

        )

        for product in products:
            PetShopOrder.objects.create(
                user_order=order,
                price=product.price,

                product=product
            )
            order.products.add(product)

        tran = create_transaction(
            user=validated_data.get("user"),
            amount=(order.total_price-((order.total_price*discount_percentage)/100))+shipping.price,
            order=order,
            transaction_type="order",
            description="some description"
        )
        order.status = Choices.Order.PAY_PENDING

        return tran