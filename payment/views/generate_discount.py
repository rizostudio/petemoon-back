from rest_framework.views import APIView
from payment.serializers import DiscountSerializer
from accounts.views.permissions import IsPetShop
from config.responses import SuccessResponse, UnsuccessfulResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from payment.models import Discount
from datetime import datetime
from django.utils.timezone import localdate

class DiscountCalculator(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        try:
            discount = Discount.objects.get(code=data['code'])
            #print( datetime.now() )
            #print(localdate())
            #print(discount.created_at)
            #print(discount.expiration_day)
            #r = (discount.created_at-localdate()).seconds
            discount_percentage = discount.percentage
            return SuccessResponse(data={'status': True, 'discount_percentage': discount_percentage })
        except Discount.DoesNotExist:
            return UnsuccessfulResponse(errors="discount matching does not exist", status_code=status.HTTP_406_NOT_ACCEPTABLE)






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
