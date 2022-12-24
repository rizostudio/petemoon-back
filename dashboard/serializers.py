from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Pet,Address


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


class PetSerializer(serializers.Serializer):
    pass


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'province',
            'city',
            'receiver',
            'postal_code',
            'postal_address'
        ]
        read_only_fields = (
            'user', 
        )

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]
        