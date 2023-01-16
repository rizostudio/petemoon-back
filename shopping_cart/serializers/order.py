from rest_framework import serializers


# class ProductInCartSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     price = serializers.IntegerField(read_only=True)
#     price_after_sale = serializers.IntegerField(read_only=True)
#     petshop = serializers.CharField(source='petshop.name',read_only=True)
#     picture = serializers.ImageField(source='product.picture',read_only=True)
#     count = serializers.IntegerField()
#     products_accumulative_price = serializers.IntegerField(read_only=True)
#     total_price = serializers.IntegerField(read_only=True)
