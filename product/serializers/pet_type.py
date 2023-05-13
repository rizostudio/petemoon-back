from rest_framework import serializers

from dashboard.models import PetCategory, PetType


class PetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetType
        fields = "__all__"


class PetCategorySerializer(serializers.ModelSerializer):
    pet_type = PetTypeSerializer(read_only=True)

    class Meta:
        model = PetCategory
        fields = "__all__"
