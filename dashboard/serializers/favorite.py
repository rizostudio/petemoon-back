from rest_framework import serializers
from dashboard.models import Favorite, Product


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=256)
    price = serializers.FloatField()
    discount = serializers.FloatField()


class FavoriteSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(write_only=True)
    product = ProductSerializer(read_only=True)

    def create(self, validated_data):
        product = Product.objects.get(id=validated_data.get('product_id'))
        favorite = Favorite.objects.create(product=product, user=self.context['request'].user)
        return favorite
