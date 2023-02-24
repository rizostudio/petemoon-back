from django.db.models import Avg, Max, Min, Sum
from django.db.models.functions import Coalesce
from rest_framework import serializers

from product.models import Product
from product.serializers.brand import BrandSerializer
from product.serializers.category import CategorySerializer
from product.serializers.comments import CommentSerializer
from product.serializers.pet_type import PetCategorySerializer
from product.serializers.petshop import PetshopSerializer
from product.serializers.pricing import ProductPricingSerializer


class ProductGetSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    productpricing = serializers.SerializerMethodField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)
    pet_type = PetCategorySerializer(read_only=True)
    best_pricing = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "name",
            "category",
            "pet_type",
            "picture",
            "details",
            "specs",
            "brand",
            "rating",
            "price",
            "comments",
            "productpricing",
            "best_pricing",
        )

    def get_price(self, obj):
        return (
            obj.price
            if hasattr(obj, "price")
            else obj.productpricing_set.filter(inventory__gt=0)
            .aggregate(price_min=Min(Coalesce("price_after_sale", "price")))
            .get("price_min")
        )

    def get_best_pricing(self, obj):
        best_price = self.get_price(obj)
        if best_price is None:
            return None
        return ProductPricingSerializer(
            (
                obj.productpricing_set.filter(
                    inventory__gt=0, price=best_price
                )
                | obj.productpricing_set.filter(
                    inventory__gt=0, price_after_sale=best_price
                )
            ).first()
        ).data

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


class ProductListSerializer(serializers.ModelSerializer):
    best_seller = serializers.SerializerMethodField(read_only=True)
    min_price = serializers.SerializerMethodField(read_only=True)
    max_price = serializers.SerializerMethodField(read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)
    inventory = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = (
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
