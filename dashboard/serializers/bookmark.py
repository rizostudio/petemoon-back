from rest_framework import serializers
from dashboard.models import Bookmark


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=256)
    price = serializers.FloatField()
    discount = serializers.FloatField()


class BookmarkSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    product = ProductSerializer(read_only=True)

    def create(self, validated_data):
        bookmark = Bookmark.objects.create(**validated_data)
        return bookmark
