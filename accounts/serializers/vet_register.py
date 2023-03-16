from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
from rest_framework import serializers



class VetRegisterSerializer(serializers.Serializer):
    medical_number = serializers.CharField(max_length=10,required=False)

    national_card_front = serializers.FileField(required=False)
    national_card_back = serializers.FileField(required=False)
    birth_certificate = serializers.FileField(required=False)
    medical_card = serializers.FileField(required=False)
    military_card = serializers.FileField(required=False) 

    gender = serializers.CharField(max_length=64, required=False)
    birth_date = serializers.DateTimeField(required=False)
    university = serializers.CharField(max_length=255,required=False)
    expertise = serializers.CharField(max_length=255, required=False)
    pet_type_experience = serializers.CharField(max_length=255, required=False)
    pet_category_fav = serializers.CharField(max_length=255,required=False)


    def update(self, instance, validated_data):
        instance.update(**validated_data)

        return instance