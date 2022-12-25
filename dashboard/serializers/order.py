from rest_framework import serializers
from dashboard.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = (
            'address',
        )
