import json
import requests
from django.shortcuts import redirect
from django.db import transaction 
from django.db.models import F
from rest_framework.views import APIView
from config.responses import bad_request, SuccessResponse, UnsuccessfulResponse
from payment.models import Transaction, PetshopSaleFee
from utils.choices import Choices
from rest_framework import status
from dashboard.models import Wallet
from rest_framework import exceptions, status
from rest_framework.response import Response
from django.conf import settings




class WalletVerifyTransaction(APIView):
    @transaction.atomic
    def get(self, *args, **kwargs):
        status = self.request.query_params.get("Status")
        authority = self.request.query_params.get("Authority")
        wallet_id = kwargs.get("walletID")

        if not authority or status != "OK":
            return redirect('https://petemoon.com/payment/status/Faild')

        try:
            wallet = Wallet.objects.get(id=wallet_id)
        except Wallet.DoesNotExist:
            return bad_request("Wallet does not exist or something wrong")

        data = {
            "MerchantID": settings.ZARRINPAL_MERCHANT_ID,
            "Amount": wallet.charge,
            "Authority": authority,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        response = requests.post(settings.ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                wallet.charge_ref_id = response['RefID']
                wallet.credit += wallet.charge
                wallet.save()
                return redirect('https://petemoon.com/payment/status/Success/?RefID={}'.format(response['RefID']))
            else:
                return SuccessResponse(data={'status': False, 'details': 'Visit has already been verified' })
        return SuccessResponse(data=response.content)


