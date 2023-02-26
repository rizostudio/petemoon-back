from rest_framework import serializers

from payment.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "amount",
            "description",
            "transaction_type",
            "order",
            "ref_id",
            "success",
            "created_at",
            "updated_at",
        )
