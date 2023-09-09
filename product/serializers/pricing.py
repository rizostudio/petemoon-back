from rest_framework import serializers
from product.models import ProductPricing
from product.serializers import PetshopSerializer
from product.models import Product


class GetProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductPricingSerializer(serializers.ModelSerializer):
    petshop = PetshopSerializer(read_only=True)
    product = GetProductSerializer(read_only=True)
    picture = serializers.ImageField(source='product.picture')
    class Meta:
        model = ProductPricing
        fields = ("id", "product", "price", "price_after_sale", "inventory", "petshop", "picture")


class AddPricingSerializer(serializers.Serializer):
    price = serializers.IntegerField(required=True)
    inventory = serializers.IntegerField(required=True)

    class Meta:
        fields = ("price", "inventory")
