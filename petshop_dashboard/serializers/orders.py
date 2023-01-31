from rest_framework import serializers

from shopping_cart.models import Order
from product.serializers.pricing import ProductPricingSerializer
from dashboard.models import Address
from dashboard.serializers import AddressSerializer


class PetShopOrdersSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order_id = serializers.CharField()
    #status = serializers.CharField()
    #address = AddressSerializer()
    product = ProductPricingSerializer()
    #total_price = serializers.IntegerField()
    #created_at = serializers.DateTimeField()
    #products_count = serializers.IntegerField()

