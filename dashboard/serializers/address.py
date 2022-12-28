from rest_framework import serializers
from dashboard.models import Address


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
