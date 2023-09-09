from rest_framework import serializers

from shopping_cart.models import Order, PetShopOrder
from product.serializers.pricing import ProductPricingSerializer
from dashboard.models import Address
from dashboard.serializers import AddressSerializer

class PetShopOrdersSerializer(serializers.ModelSerializer):
    product = ProductPricingSerializer()
    class Meta:
        model = PetShopOrder
        fields = '__all__'



class OrdersSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order_id = serializers.CharField()
    status = serializers.CharField()
    product = PetShopOrdersSerializer(many=True)
    total_price = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    products_count = serializers.IntegerField()



class ProductsSerializer(serializers.Serializer):
    image = serializers.ImageField()
    name = serializers.CharField()
    count = serializers.IntegerField()
    discount = serializers.IntegerField()
    total_price = serializers.IntegerField()

class UserDetailsSerializer(serializers.Serializer):
    name = serializers.CharField(source='user.first_name')
    order_date = serializers.DateTimeField(source='created_at')
    order_id = serializers.CharField()
    reciver = serializers.CharField(source='address.receiver')



class OrderSingleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order_id = serializers.CharField()
    status = serializers.CharField()
    total_price = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    products_count = serializers.IntegerField()
