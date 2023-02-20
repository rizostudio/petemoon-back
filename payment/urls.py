from django.urls import path

from payment.views import GetTransactionList, VerifyTransaction

urlpatterns = [
    path("", GetTransactionList.as_view(), name="get-transaction-list"),
    path(
        "verify/<int:transaction_id>/",
        VerifyTransaction.as_view(),
        name="verify-transaction",
    ),
]
