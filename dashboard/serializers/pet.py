from rest_framework import serializers
from dashboard.models import Pet


class PetMidicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = [
            'name',
            'type',
            'sex',
            'species',
            'birth_date',
        ]


class PetGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = [
            'weight',
            'last_vaccine_date',
            'underlying_disease',
            'last_anti_parasitic_vaccine_date',
        ]