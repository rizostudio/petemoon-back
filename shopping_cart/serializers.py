from rest_framework import serializers


class CartSerializer(serializers.Serializer):
    product_pricing_id = serializers.IntegerField()
    count = serializers.IntegerField()
