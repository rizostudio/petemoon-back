from django.urls import path
from payment.views import GetTransactionList, VerifyTransaction, SendReqTransaction, GenerateDiscount, DiscountCalculator

urlpatterns = [
    path("generate-discount/",GenerateDiscount.as_view(),name="generate-discount"),
    path("discount-calculator/",DiscountCalculator.as_view(),name="discount-calculator"),
    path("", GetTransactionList.as_view(), name="get-transaction-list"),
    path("send-req/<int:transaction_id>/",SendReqTransaction.as_view(),name="send-req-transaction"),
    path("verify/<int:transaction_id>/",VerifyTransaction.as_view(),name="verify-transaction"),
]
