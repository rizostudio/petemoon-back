from django.db.models import Avg, Min
from django.db.models.functions import Coalesce
from rest_framework import serializers

from product.models import Product
from product.serializers.brand import BrandSerializer
from product.serializers.category import CategorySerializer
from product.serializers.comments import CommentSerializer
from product.serializers.pricing import ProductPricingSerializer


class ProductGetSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    productpricing = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "name",
            "category",
            "animal_type",
            "picture",
            "details",
            "specs",
            "brand",
            "rating",
            "price",
            "comments",
            "productpricing",
        )

    def get_price(self, obj):
        return (
            obj.price
            if hasattr(obj, "price")
            else obj.productpricing_set.filter(inventory__gt=0)
            .aggregate(price_min=Min(Coalesce("price_after_sale", "price")))
            .get("price_min")
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

    def get_comments(self, obj):
        return CommentSerializer(
            obj.comments.filter(published=True), many=True
        ).data
