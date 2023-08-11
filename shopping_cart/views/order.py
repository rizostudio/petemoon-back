from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions
from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException
from ..utils import get_cart
from product.models.pricing import ProductPricing
from ..serializers import OrderGetSerializer, OrderPostSerializer
from shopping_cart.models import Order, Shipping
from dashboard.models import Address
import json
import requests
from django.conf import settings
from django.db import transaction
from django.db.models import F
from payment.models import Transaction, PetshopSaleFee
from utils.choices import Choices
from rest_framework.response import Response
from rest_framework import status




class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        try:
            try:
                order = Order.objects.get(id=id, user=request.user)
            except:
                raise CustomException(detail=_("Order does not exist"))

            serialized_data = OrderGetSerializer(order).data
            return SuccessResponse(data=serialized_data)
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)



    def post(self, request):
        # add method post to total price
        serialized_data = OrderPostSerializer(data=request.data)

        try:
            if serialized_data.is_valid(raise_exception=True):
                
                cart = get_cart(request.user.id)
                if cart == None:
                    return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data='Your shopping cart is empty')
                  
                try:
                    shipping_method = Shipping.objects.get(id=request.data['shipping_method'])
                except Shipping.DoesNotExist:
                    return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data='Shipping matching does not exist')

                try:
                    address = Address.objects.get(id=cart['address'],user=request.user)
                except Address.DoesNotExist:
                    return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data='Address matching does not exist')

                else:
                    products = []
                    total_price = 0
                    for key, value in cart['products'].items():
                        product_in_cart = ProductPricing.objects.get(id=key)
                        products.append(product_in_cart)
                        product_in_cart.count = value
                        product_in_cart.products_accumulative_price = product_in_cart.count * \
                            product_in_cart.price
                        total_price += product_in_cart.products_accumulative_price

                tran = serialized_data.save(user=request.user, total_price=total_price, products=products, address=address)

                try:
                    transaction = Transaction.objects.latest('id')
                    #transaction = Transaction.objects.get(id=tran['transaction'], success=False)
                except Transaction.DoesNotExist:
                    return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data='Transaction does not exist or has already been verified.')

                data = {
                    "MerchantID": settings.ZARRINPAL_MERCHANT_ID,
                    "Amount": transaction.amount,
                    "Description": transaction.description,
                    "CallbackURL": settings.ZARIN_CALL_BACK + str(transaction.id) + "/",
                    "TransactionID": transaction.id}
                data = json.dumps(data)
                headers = {'content-type': 'application/json', 'content-length': str(len(data))}

                try:
                    response = requests.post(settings.ZP_API_REQUEST, data=data, headers=headers, timeout=10)
                    if response.status_code == 200:
                        response = response.json()
                        if response['Status'] == 100:
                            transaction.authority = response['Authority']
                            transaction.save()

                            c={'status': True, 'url': settings.ZP_API_STARTPAY + str(response['Authority']), 'transaction': transaction.id, 'authority': response['Authority']}
                            return Response(data=c, status=status.HTTP_200_OK)
                            '''
                            return SuccessResponse(
                                data={'status': True, 'url': settings.ZP_API_STARTPAY + str(response['Authority']),
                                      'transaction': transaction.id, 'authority': response['Authority']})
                            '''
                        else:
                            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data='errrr')
                            #return {'status': False, 'code': str(response['Status'])}
                except:
                    return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data='connection error or timeout')

        except:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data='error')
