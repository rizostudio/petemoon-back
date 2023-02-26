import requests
from django.db import transaction as db_transaction
from django.db.models import F
from rest_framework.views import APIView

from config.responses import bad_request, ok
from config.settings import ZARRINPAL_MERCHANT_ID, ZARRINPAL_URL
from payment.models import Transaction


class VerifyTransaction(APIView):
    @db_transaction.atomic
    def get(self, *args, **kwargs):
        authority = self.request.query_params.get("Authority")
        OK = self.request.query_params.get("Status") == "OK"
        transaction_id = kwargs.get("transaction_id")
        if not authority or not OK:
            return bad_request("invalid request")
        if Transaction.objects.filter(
            authority=authority, id=transaction_id
        ).exists():
            return bad_request("transaction doesn't exist")
        transaction = Transaction.objects.get(id=transaction_id)
        response = requests.post(
            f"{ZARRINPAL_URL}v4/payment/verify.json",
            json={
                "merchant_id": ZARRINPAL_MERCHANT_ID,
                "amount": transaction.amount,
                "authority": authority,
            },
        )
        data = response.json()
        if (
            data["data"]["code"] != 100
            and data["data"]["code"] != 101
            and data["data"]["message"] != "Verified"
        ):
            return bad_request("invalid request")
        transaction.success = True
        transaction.ref_id = data["data"]["ref_id"]
        transaction.save()
        if transaction.transaction_type == "wallet":
            user = transaction.user
            if user.user_type == "normal":
                profile = user.profile
                profile.wallet = transaction.amount + F("wallet")
                profile.save()
        return ok("transaction verified successfully")
