from rest_framework import serializers
from dashboard.serializers import PetSerializer



class MyOrdersSerializer(serializers.Serializer):
    ongoing_orders = serializers.IntegerField()
    canceled_orders = serializers.IntegerField()
    delivered_orders = serializers.IntegerField()


class OverViewSerializer(serializers.Serializer):
    wallet = serializers.IntegerField(read_only=True)
    pet = PetSerializer()
    order_count = serializers.IntegerField(read_only=True)
    order_total_price = serializers.EmailField()
    my_orders = MyOrdersSerializer()

  
