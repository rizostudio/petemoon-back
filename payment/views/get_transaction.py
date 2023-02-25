from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from config.responses import ok
from payment.serializers import TransactionSerializer


class GetTransactionList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = request.user.transactions.all()
        serializer = TransactionSerializer(transactions, many=True)
        return ok(serializer.data)
