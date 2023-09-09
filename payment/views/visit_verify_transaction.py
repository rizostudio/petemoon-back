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
from vet.models import Visit


class VisitVerifyTransaction(APIView):
    @transaction.atomic
    def get(self, *args, **kwargs):
        status = self.request.query_params.get("Status")
        authority = self.request.query_params.get("Authority")
        visit_id = kwargs.get("visitID")

        if not authority or status != "OK":
            return redirect('https://petemoon.com/payment/status/Faild')

        try:
            visit = Visit.objects.get(id=visit_id)
        except Visit.DoesNotExist:
            return bad_request("Visit does not exist or has already been verified.")

        data = {
            "MerchantID": settings.ZARRINPAL_MERCHANT_ID,
            "Amount": visit.price,
            "Authority": authority,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        response = requests.post(settings.ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                visit.status = 'DONE'
                visit.authority = authority
                visit.ref_id = response['RefID']
                visit.save()
                return redirect('https://petemoon.com/payment/status/Success/?RefID={}'.format(response['RefID']))
            else:
                return SuccessResponse(data={'status': False, 'details': 'Visit has already been verified' })
        return SuccessResponse(data=response.content)


