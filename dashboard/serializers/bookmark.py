from rest_framework import serializers
from dashboard.models import Bookmark
from product.serializers import ProductGetSerializer


class BookmarkSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    product = ProductGetSerializer(read_only=True)

    def create(self, validated_data):
        bookmark = Bookmark.objects.create(**validated_data)
        return bookmark
