from rest_framework import serializers


class ProductsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(source="product.name", read_only=True)
    picture = serializers.ImageField(source="product.picture", read_only=True)
    slug = serializers.CharField(source="product.slug", read_only=True)
    price = serializers.IntegerField()
    price_after_sale = serializers.IntegerField()
    inventory = serializers.IntegerField()

    def update(self, instance, validated_data):
        instance.update(**validated_data)

        return instance
