from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
from rest_framework import serializers

national_id_validator = RegexValidator(
    r"^\d{10}$", message=_("Invalid national ID.")
)
sheba_number_validator = RegexValidator(
    r"^IR\d{24}$", message=_("Invalid sheba.")
)


class PetShopRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=200,required=True)
    last_name = serializers.CharField(max_length=200,required=True)
    address = serializers.CharField(max_length=200,required=False)
    description = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    city = serializers.CharField(max_length=64,required=False)
    province = serializers.CharField(max_length=64, required=False)
    postal_region = serializers.CharField(max_length=64,required=False)
 
    national_id = serializers.CharField(
        max_length=10,
        validators=[national_id_validator],
    required=False
    )

    #files
    national_card = serializers.FileField(required=False)
    birth_certificate = serializers.FileField(required=False)
    business_license = serializers.FileField(required=False)
    union_license = serializers.FileField(required=False)
    tax_certificate = serializers.FileField(required=False)

    estimated_item_count = serializers.IntegerField(required=False)
    gender = serializers.CharField(max_length=64,required=False)
 
    sheba_number = serializers.CharField(
        max_length=26,validators=[sheba_number_validator],required=False)
    
    def update(self, instance, validated_data):
        instance.update(**validated_data)

        return instance