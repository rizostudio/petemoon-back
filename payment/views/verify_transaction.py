import json
import requests

from django.conf import settings
from django.db import transaction 
from django.db.models import F
from rest_framework.views import APIView

from config.responses import bad_request, SuccessResponse, UnsuccessfulResponse
from payment.models import Transaction
from utils.choices import Choices


class VerifyTransaction(APIView):
    @transaction.atomic
    def get(self, *args, **kwargs):
        authority = self.request.query_params.get("Authority")
        status = self.request.query_params.get("Status")
        transaction_id = kwargs.get("transaction_id")

        if not authority or status != "OK":
            return bad_request("Invalid request")

        try:
            transaction = Transaction.objects.select_for_update().get(
                id=transaction_id,
                authority=authority,
                success=False,
            )
        except Transaction.DoesNotExist:
            return bad_request("Transaction does not exist or has already been verified.")

        data = {
            "MerchantID": settings.ZARRINPAL_MERCHANT_ID,
            "Amount":  transaction.amount,
            "Authority": authority,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }

        response = requests.post(
            f"{settings.ZARRINPAL_URL}/pg/rest/WebGate/PaymentVerification.json",
            data=data,
            headers=headers,
        )
        response_data = response.json()

        if response.status_code != 200:
            return UnsuccessfulResponse(errors=response_data,status_code=response.status_code)

        transaction.success = True
        transaction.ref_id = response_data["data"]["ref_id"]
        transaction.save()

        if transaction.transaction_type == "wallet":
            user = transaction.user
            if user.user_type == "normal":
                profile = user.profile
                profile.wallet = transaction.amount + F("wallet")
                profile.save()

        if transaction.transaction_type == "order":
            transaction.order.status = Choices.Order.PROCESSING
            transaction.order.save()

        return SuccessResponse(data=response_data)
