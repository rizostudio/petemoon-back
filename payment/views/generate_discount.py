from rest_framework.views import APIView
from payment.serializers import DiscountSerializer
from accounts.views.permissions import IsPetShop
from config.responses import SuccessResponse, UnsuccessfulResponse
from rest_framework import status


class GenerateDiscount(APIView):
    permission_classes = [IsPetShop]

    def post(self, request):
        return UnsuccessfulResponse(errors='This option has been deactivated', status_code=status.HTTP_406_NOT_ACCEPTABLE)
        '''
        data = request.data
        data['creator'] = request.user.id
        serializer = DiscountSerializer(data=data)
        if serializer.is_valid():
            serializer.validated_data
            serializer.save()
            return SuccessResponse(data={'status': True, 'data': serializer.data })
        else:
            return UnsuccessfulResponse(errors=serializer.errors, status_code=status.HTTP_406_NOT_ACCEPTABLE)
        '''
