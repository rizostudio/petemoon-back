from rest_framework import serializers
from payment.services.create_transaction import create_transaction

class WalletSerializer(serializers.Serializer):
    credit = serializers.IntegerField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    add_value = serializers.IntegerField(write_only=True)
    
    def create(self, validated_data):
        create_transaction(user=validated_data['user'],amount=validated_data['add_value'],transaction_type="wallet")
        validated_data['user'].profile.wallet.credit += validated_data['add_value']

        return validated_data['user'].profile.wallet
