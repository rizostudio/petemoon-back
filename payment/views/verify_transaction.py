import json
import requests

from django.conf import settings
from django.db import transaction 
from django.db.models import F
from rest_framework.views import APIView

from config.responses import bad_request, SuccessResponse, UnsuccessfulResponse
from payment.models import Transaction
from utils.choices import Choices




class SendReqTransaction(APIView):
    @transaction.atomic
    def get(self, *args, **kwargs):
        authority = self.request.query_params.get("Authority")
        status = self.request.query_params.get("Status")
        transaction_id = kwargs.get("transaction_id")

        #if not authority or status != "OK":
            #return bad_request("Invalid request")

        try:
            transaction = Transaction.objects.get(id=transaction_id,success=False)
        except Transaction.DoesNotExist:
            return bad_request("Transaction does not exist or has already been verified.")

        data = {
            "MerchantID": settings.ZARRINPAL_MERCHANT_ID,
            "Amount": transaction.amount,
            "Description": transaction.description,
            "Authority": authority,
            "CallbackURL": settings.ZARIN_CALL_BACK,
            "TransactionID": transaction.id,
        }

        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }

        try:
            response = requests.post(settings.ZP_API_REQUEST, data=data, headers=headers, timeout=10)

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
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

        print(authority)

        data = {
            "MerchantID": settings.ZARRINPAL_MERCHANT_ID,
            "Authority": authority
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return {'status': True, 'RefID': response['RefID']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response







        authority = self.request.query_params.get("Authority")
        status = self.request.query_params.get("Status")
        transaction_id = kwargs.get("transaction_id")

        if not authority or status != "OK":
            return bad_request("Invalid request")

        try:
            transaction = Transaction.objects.get(id=transaction_id, success=False)
        except Transaction.DoesNotExist:
            return bad_request("Transaction does not exist or has already been verified.")

        data = {
            "MerchantID": settings.ZARRINPAL_MERCHANT_ID,
            "Amount": transaction.amount,
            "Description": transaction.description,
            "Authority": authority,
            "CallbackURL": settings.ZARIN_CALL_BACK,
        }

        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}

        try:
            response = requests.post(settings.ZP_API_REQUEST, data=data, headers=headers, timeout=10)

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    return SuccessResponse(
                        data={'status': True, 'url': settings.ZP_API_STARTPAY + str(response['Authority']),
                              'authority': response['Authority']})
                else:
                    return {'status': False, 'code': str(response['Status'])}
            return response

        except requests.exceptions.Timeout:
            return {'status': False, 'code': 'timeout'}
        except requests.exceptions.ConnectionError:
            return {'status': False, 'code': 'connection error'}


        response = requests.post(f"{settings.ZARRINPAL_URL}StartPay/",
            data=data,
            headers=headers,
        )

        if response.status_code == 200:
            response = response.json()
            transaction.success = True
            transaction.authority = authority
            transaction.ref_id = response["data"]["ref_id"]
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

            if response['Status'] == 100:
                return SuccessResponse(data={"RefID": response['RefID'] })
                #return {'status': True, 'RefID': response['RefID']}
            else:
                return UnsuccessfulResponse()
                #return {'status': False, 'code': str(response['Status'])}

        return SuccessResponse(data=response.content)
