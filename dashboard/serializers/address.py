from rest_framework import serializers
from dashboard.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        
        read_only_fields = (
            'user',
        )

    def create(self, validated_data):
        addres = Address.objects.create(**validated_data)
        return addres

    def update(self, instance, validated_data):
        instance.update(**validated_data)

        return instance