from rest_framework import serializers
from dashboard.models import Favorite


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=256)
    price = serializers.FloatField()
    discount = serializers.FloatField()


class FavoriteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    product = ProductSerializer(read_only=True)

    def create(self, validated_data):
        favorite = Favorite.objects.create(**validated_data)
        return favorite
