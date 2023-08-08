from rest_framework import serializers
from payment.models import Transaction, Discount

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ("code", "creator", "percentage", "expiration_day")


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
