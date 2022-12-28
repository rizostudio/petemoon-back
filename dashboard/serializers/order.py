from rest_framework import serializers
from dashboard.models import Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['order_id','status','address','product']
        read_only_fields = (
            'address',
        )
        depth = 1

