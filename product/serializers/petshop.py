from django.db.models import Avg
from rest_framework import serializers

from product.models import Comment, Petshop


class PetshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Petshop
        fields = ("name", "slug")


class PetshopGetSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Petshop
        fields = ("name", "slug", "average_rating")

    def get_average_rating(self, obj):
        return Comment.objects.filter(product__petshop=obj).aggregate(
            avg_rating=Avg("rate")
        )["avg_rating"]
