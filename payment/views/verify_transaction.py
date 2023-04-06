import requests
from django.db import transaction 
from django.db.models import F
from rest_framework.views import APIView

from config.responses import bad_request, ok
from config.settings import ZARRINPAL_MERCHANT_ID, ZARRINPAL_URL
from payment.models import Transaction
from django.conf import settings
import json
from config.responses import SuccessResponse,UnsuccessfulResponse


class VerifyTransaction(APIView):
    @transaction.atomic
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
        print(transaction.amount)
   
        data = {
        "MerchantID": settings.ZARRINPAL_MERCHANT_ID,
        "Amount":  transaction.amount,
        "Authority": authority,
            }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response = requests.post("https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json", data=data,headers=headers)
        response_data = response.json()
        if response.status_code == 200:
            transaction.success = True
            transaction.ref_id = response_data["data"]["ref_id"]
            transaction.save()
            if transaction.transaction_type == "wallet":
                user = transaction.user
                if user.user_type == "normal":
                    profile = user.profile
                    profile.wallet = transaction.amount + F("wallet")
                    profile.save()
            response = response.json()
            if response['Status'] == 100:
                return SuccessResponse (data=response_data)
            else:
                return UnsuccessfulResponse (errors=response_data,status_code=400)
        
    
    

        
