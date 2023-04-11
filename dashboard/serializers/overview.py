from rest_framework import serializers


class MyOrdersSerializer(serializers.Serializer):
    ongoing_orders = serializers.IntegerField()
    canceled_orders = serializers.IntegerField()
    delivered_orders = serializers.IntegerField()


