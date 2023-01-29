from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
from rest_framework import serializers

national_id_validator = RegexValidator(
    r"^\d{10}$", message=_("Invalid national ID.")
)
sheba_number_validator = RegexValidator(
    r"^IR\d{24}$", message=_("Invalid sheba.")
)


class Stage0PetShopSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=64, required=True)
    last_name = serializers.CharField(max_length=64, required=True)
    gender = serializers.CharField(max_length=64, required=True)
    national_id = serializers.CharField(
        max_length=10, required=True, validators=[national_id_validator]
    )

    class Meta:
        fields = "__all__"


class Stage1PetShopSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=64, required=True)
    postal_region = serializers.CharField(max_length=64, required=True)
    address = serializers.CharField(max_length=200, required=True)
    store_name = serializers.CharField(max_length=64, required=True)

    class Meta:
        fields = "__all__"


class Stage2PetShopSerializer(serializers.Serializer):
    sheba_number = serializers.CharField(
        max_length=26, validators=[sheba_number_validator], required=True
    )
    estimated_item_count = serializers.IntegerField(min_value=1, required=True)

    class Meta:
        fields = "__all__"
