from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
from rest_framework import serializers

national_id_validator = RegexValidator(
    r"^\d{10}$", message=_("Invalid national ID.")
)
sheba_number_validator = RegexValidator(
    r"^IR\d{24}$", message=_("Invalid sheba.")
)


class VetRegisterSerializer(serializers.Serializer):
    medical_number = serializers.CharField(max_length=10)

    national_card_front = serializers.FileField()
    national_card_back = serializers.FileField()
    birth_certificate = serializers.FileField()
    medical_card = serializers.FileField()
    military_card = serializers.FileField() 

    gender = serializers.CharField(max_length=64, )
    birth_date = serializers.DateTimeField()
    university = serializers.CharField(max_length=255)
    expertise = serializers.CharField(max_length=255)
    pet_type_experience = serializers.CharField(max_length=255)
    pet_category_fav = serializers.CharField(max_length=255)


    def update(self, instance, validated_data):
        instance.update(**validated_data)

        return instance