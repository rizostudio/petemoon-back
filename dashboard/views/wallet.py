from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from dashboard.serializers import WalletSerializer
from dashboard.models import Pet, Wallet
from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException
from rest_framework import exceptions, status
from rest_framework.response import Response
import json
import requests
from django.conf import settings


class WalletView(APIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet = Wallet.objects.get(user=self.request.user)
        result = self.serializer_class(self.request.user.profile.wallet).data
        return SuccessResponse(data=wallet.credit)


    def post(self, request):
        charge = request.data['charge']
        wallet = Wallet.objects.get(user=self.request.user)
        wallet.charge = charge
        wallet.save()

        data = {
            "MerchantID": settings.ZARRINPAL_MERCHANT_ID,
            "Amount": charge,
            "Description": ' شارژ کیف پول',
            "CallbackURL": settings.ZARIN_CALL_BACK_WALLET + str(wallet.id) + "/",
            'walletID': wallet.id,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        try:
            response = requests.post(settings.ZP_API_REQUEST, data=data, headers=headers, timeout=10)
            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    response_data = {'status': True, 'walletID': wallet.id, 'amount': charge,
                            'authority': response['Authority'], 'description':' شارژ کیف پول'  ,
                            'url': settings.ZP_API_STARTPAY + str(response['Authority'])}
                    return Response(response_data, status=status.HTTP_200_OK)


                else:
                    return {'status': False, 'code': str(response['Status'])}
            return response

        except requests.exceptions.Timeout:
            return {'status': False, 'code': 'timeout'}
        except requests.exceptions.ConnectionError:
            return {'status': False, 'code': 'connection error'}






        '''
        serialized_data = self.serializer_class(data=request.data)
        try:
            if serialized_data.is_valid(raise_exception=True):
                wallet = serialized_data.save(user=request.user)
                return SuccessResponse(data=self.serializer_class(wallet).data)
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        '''


class VerifyWalletView(APIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]