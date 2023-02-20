from django.urls import path

from payment.views import VerifyTransaction

urlpatterns = [
    path("verify/<int:transaction_id>/", VerifyTransaction.as_view()),
]
