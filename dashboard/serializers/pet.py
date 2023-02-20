from rest_framework import serializers
from dashboard.models import Pet, PetType, PetCategory


class PetTypeSerializer(serializers.ModelSerializer):
    pass


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    pet_type = serializers.CharField(source='pet_type.pet_type',required=False)
    sex = serializers.CharField(max_length=1)
    pet_category = serializers.CharField(source='pet_category.pet_category',required=False)
    birth_date = serializers.DateField()
    # medical
    weight = serializers.FloatField(required=False)
    last_vaccine_date = serializers.DateField(required=False)
    underlying_disease = serializers.CharField(required=False)
    last_anti_parasitic_vaccine_date = serializers.DateField(required=False)

    def create(self, validated_data):
        validated_data['pet_type'] = PetType.objects.get(
            pet_type=validated_data['pet_type']['pet_type'])
        validated_data['pet_category'] = PetCategory.objects.get(
            pet_category=validated_data['pet_category']['pet_category'])

        pet = Pet.objects.create(**validated_data)
        return pet

    def update(self, instance, validated_data):
        instance.update(**validated_data)

        return instance
