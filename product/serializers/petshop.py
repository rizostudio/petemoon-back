from rest_framework import serializers

from product.models import Petshop


class PetshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Petshop
        fields = ("name", "slug")
