from rest_framework import serializers

from dashboard.models import PetCategory, PetType


class PetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetType
        fields = ("pet_type",)


class PetCategorySerializer(serializers.ModelSerializer):
    pet_type = PetTypeSerializer(read_only=True)

    class Meta:
        model = PetCategory
        fields = ("pet_category", "pet_type")
