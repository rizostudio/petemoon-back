import json
import requests
from django.shortcuts import redirect
from django.conf import settings
from django.db import transaction 
from django.db.models import F
from rest_framework.views import APIView
from config.responses import bad_request, SuccessResponse, UnsuccessfulResponse
from payment.models import Transaction, PetshopSaleFee
from utils.choices import Choices
from rest_framework.response import Response
from rest_framework import status



class SendReqTransaction(APIView):
    @transaction.atomic
    def get(self, *args, **kwargs):
        authority = self.request.query_params.get("Authority")
        status = self.request.query_params.get("Status")
        transaction_id = kwargs.get("transaction_id")

        try:
            transaction = Transaction.objects.get(id=transaction_id,success=False)
        except Transaction.DoesNotExist:
            return bad_request("Transaction does not exist or has already been verified.")

        data = {
            "MerchantID": settings.ZARRINPAL_MERCHANT_ID,
            "Amount": transaction.amount,
            "Description": transaction.description,
            "Authority": authority,
            "CallbackURL": settings.ZARIN_CALL_BACK
                   + str(transaction.id)
                   + "/",
            "TransactionID": transaction.id,
        }

        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }

        try:
            response = requests.post(settings.ZP_API_REQUEST, data=data, headers=headers, timeout=10)

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    transaction.authority = response['Authority']
                    transaction.save()
                    return SuccessResponse(data= {'status': True, 'url': settings.ZP_API_STARTPAY + str(response['Authority']), 'transaction': transaction.id, 'authority': response['Authority']})
                else:
                    return {'status': False, 'code': str(response['Status'])}
            return response

        except requests.exceptions.Timeout:
            return {'status': False, 'code': 'timeout'}
        except requests.exceptions.ConnectionError:
            return {'status': False, 'code': 'connection error'}



class VerifyTransaction(APIView):
    @transaction.atomic
    def get(self, *args, **kwargs):
        status = self.request.query_params.get("Status")
        authority = self.request.query_params.get("Authority")
        transaction_id = kwargs.get("transaction_id")

        if not authority or status != "OK":
            return redirect('https://petemoon.com/payment/status/Faild')

        try:
            transaction = Transaction.objects.get(id=transaction_id,success=False)
        except Transaction.DoesNotExist:
            return bad_request("Transaction does not exist or has already been verified.")

        data = {
            "MerchantID": settings.ZARRINPAL_MERCHANT_ID,
            "Amount": transaction.amount,
            "Authority": authority,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        response = requests.post(settings.ZP_API_VERIFY, data=data, headers=headers)

        products = transaction.order.products.all()
        print(products)
        for product in products:
            print(product.price)
            print(product.petshop)
        print('--#---------------')
        # mojodi kam beshe

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                transaction.success = True
                transaction.authority = authority
                transaction.ref_id = response['RefID']
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
                    # PetshopSaleFee emal beshe (baresi kon shayad oonvar mishe )

                return redirect('https://petemoon.com/payment/status/Success/?RefID={}'.format(response['RefID']))
            else:
                return SuccessResponse(data={'status': False, 'details': 'Transaction has already been verified' })
        return SuccessResponse(data=response.content)


