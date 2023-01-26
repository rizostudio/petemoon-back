from rest_framework import serializers


class ProductsSerializer(serializers.Serializer):
    name = serializers.CharField(source="product.name")
    picture = serializers.ImageField(source="product.picture")
    slug = serializers.CharField(source="product.slug")
    price = serializers.IntegerField()
    inventory = serializers.IntegerField()
