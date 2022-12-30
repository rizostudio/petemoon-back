from rest_framework import serializers
from dashboard.models import Pet


class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    type = serializers.CharField()
    sex = serializers.CharField(max_length=1)
    species = serializers.CharField()
    birth_date = serializers.DateField()
    #medical
    weight = serializers.FloatField(required=False)
    last_vaccine_date = serializers.DateField(required=False)
    underlying_disease = serializers.CharField(required=False)
    last_anti_parasitic_vaccine_date = serializers.DateField(required=False)

    def create(self, validated_data):
        
        pet = Pet.objects.create(**validated_data)
        return pet

    def update(self, instance, validated_data):
        instance.update(**validated_data)

        return instance