from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from config.responses import SuccessResponse, UnsuccessfulResponse
from dashboard.serializers import WalletSerializer
from dashboard.models import Pet
from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException


class WalletView(APIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):

        result = self.serializer_class(self.request.user.profile.wallet).data
        return SuccessResponse(data=result)

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        try:
            if serialized_data.is_valid(raise_exception=True):
                wallet = serialized_data.save(user=request.user)
                return SuccessResponse(data=self.serializer_class(wallet).data)
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
