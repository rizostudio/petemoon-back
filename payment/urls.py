from django.urls import path
from payment.views import GetTransactionList, VerifyTransaction, SendReqTransaction, GenerateDiscount

urlpatterns = [
    path("generate-discount/",GenerateDiscount.as_view(),name="generate-discount"),
    path("", GetTransactionList.as_view(), name="get-transaction-list"),
    path("send-req/<int:transaction_id>/",SendReqTransaction.as_view(),name="send-req-transaction"),
    path("verify/<int:transaction_id>/",VerifyTransaction.as_view(),name="verify-transaction"),
]
