from rest_framework import serializers
from shopping_cart.models import Order
# from product.serializers.pricing import ProductPricingSerializer
from dashboard.serializers import AddressSerializer

from product.serializers.petshop import PetshopSerializer
from product.models import ProductPricing

class ProductPricingSerializer(serializers.ModelSerializer):
    petshop = PetshopSerializer(read_only=True)
    picture = serializers.ImageField(source='product.picture')
    class Meta:
        model = ProductPricing
        fields = ("id", "price", "price_after_sale", "inventory", "petshop","picture")

class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order_id = serializers.CharField()
    status = serializers.CharField()
    address = AddressSerializer()
    products = ProductPricingSerializer(many=True)
    total_price = serializers.IntegerField()
    shipping_method = "ShippingSerializer()"
