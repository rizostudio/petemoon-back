from django.urls import path

from payment.views import GetTransactionList, VerifyTransaction, SendReqTransaction

urlpatterns = [
    path("", GetTransactionList.as_view(), name="get-transaction-list"),
    path("send-req/<int:transaction_id>/",SendReqTransaction.as_view(),name="send-req-transaction"),
    path("verify/",VerifyTransaction.as_view(),name="verify-transaction"),
]
