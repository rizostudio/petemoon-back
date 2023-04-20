from rest_framework import serializers

from django.db.models import Avg, Max, Min, Sum
from django.db.models.functions import Coalesce

from product.models import Product, ProductPricing
from product.serializers.petshop import PetshopSerializer


class PetShopProductPricingSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(write_only=True)
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

    def create(self, validated_data):
        product_id = validated_data.pop('product_id')

        validated_data["product"] = Product.objects.get(id=product_id)
        product_pricing = ProductPricing.objects.create(**validated_data)


        return "product_pricing"

class ProductListSerializer(serializers.ModelSerializer):
    best_seller = serializers.SerializerMethodField(read_only=True)
    min_price = serializers.SerializerMethodField(read_only=True)
    max_price = serializers.SerializerMethodField(read_only=True)
    category = "CategorySerializer(read_only=True)"
    rating = serializers.SerializerMethodField(read_only=True)
    inventory = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "category",
            "picture",
            "best_seller",
            "min_price",
            "max_price",
            "inventory",
            "rating",
        )

    def get_min_price(self, obj):
        return (
            obj.price
            if hasattr(obj, "min_price")
            else obj.productpricing_set.filter(inventory__gt=0)
            .aggregate(price_min=Min(Coalesce("price_after_sale", "price")))
            .get("price_min")
        )

    def get_max_price(self, obj):
        return (
            obj.productpricing_set.filter(inventory__gt=0)
            .aggregate(price_max=Max("price"))
            .get("price_max")
        )

    def get_rating(self, obj):
        return (
            obj.rating
            if hasattr(obj, "rating")
            else obj.comments.filter(published=True)
            .aggregate(avg=Avg("rate"))
            .get("avg")
        )

    def get_productpricing(self, obj):
        return ProductPricingSerializer(
            obj.productpricing_set.filter(inventory__gt=0), many=True
        ).data

    def get_best_seller(self, obj):
        best_price = self.get_min_price(obj)
        if best_price is None:
            return None
        return PetshopSerializer(
            (
                obj.productpricing_set.filter(
                    inventory__gt=0, price=best_price
                )
                | obj.productpricing_set.filter(
                    inventory__gt=0, price_after_sale=best_price
                )
            )
            .first()
            .petshop
        ).data

    def get_inventory(self, obj):
        return obj.productpricing_set.aggregate(
            total_inventory=Sum("inventory")
        ).get("total_inventory")
