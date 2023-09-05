from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from ..serializers import VisitSerializer
from dashboard.models import Address
from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException
from accounts.views.permissions import IsVet
from accounts.models import VetProfile
from ..models import ReserveTimes
from vet.models import Visit
from rest_framework import viewsets, status
from rest_framework.response import Response
import json
import requests
from django.conf import settings
from django.db import transaction
from django.db.models import F
from payment.models import Transaction, PetshopSaleFee
from utils.choices import Choices
from rest_framework.response import Response
from rest_framework import status




def zp_send_request(visit_id):
    visit = Visit.objects.get(id=visit_id)
    data = {
        "MerchantID": settings.ZARRINPAL_MERCHANT_ID,
        "Amount": visit.price,
        "Description": 'پرداخت ویزیت',
        "CallbackURL": settings.ZARIN_CALL_BACK + str(visit.id) + "/",
        'transactionID': visit.id,
    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    try:
        response = requests.post(settings.ZP_API_REQUEST, data=data, headers=headers, timeout=10)
        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                return {'status': True,'visitID':visit.id, 'amount':visit.price,
                        'authority':response['Authority'],'description': visit.explanation,
                        'url': settings.ZP_API_STARTPAY + str(response['Authority']) }
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response

    except requests.exceptions.Timeout:
        return {'status': False, 'code': 'timeout'}
    except requests.exceptions.ConnectionError:
        return {'status': False, 'code': 'connection error'}







class VisitView(APIView):

    permission_classes = [IsVet]
    serializer_class = VisitSerializer

    # def get(self, request, id=None):
    #     try:
            
    #         vet = VetProfile.objects.get(user=request.user)
    #         serialized_data = self.serializer_class(vet).data
            
    #         return SuccessResponse(data=serialized_data)
    #     except CustomException as e:
    #         return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)


    def post(self, request):
        data=request.data
        data['user']=request.user.id
        serialized_data = self.serializer_class(data=data)
        try:
            if serialized_data.is_valid():
                visit_id = serialized_data.save()
                data = zp_send_request(visit_id)
                return Response(data, status=status.HTTP_200_OK)

            return SuccessResponse(data={"message":_("Visit added successfuly")})

        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)






class SingleVisitView(APIView):
    permission_classes = [IsVet]
    serializer_class = VisitSerializer

    def patch(self, request, id=None):
        visit = Visit.objects.get(id=id)
        serialized_data = self.serializer_class(visit,data=request.data, partial=True)
        try:
            if serialized_data.is_valid(raise_exception=True):
                visit_data = serialized_data.update(instance=visit,validated_data=serialized_data.validated_data)
                return Response('Visit updated.', status=status.HTTP_200_OK)
                #return SuccessResponse(data=VisitSerializer(visit).data)

        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)




    '''

    def patch(self, request, id=None):
        data = request.data
        visit = Visit.objects.get(id=id)
        data['pet'] = visit.pet.id
        data['vet'] = visit.vet.id
        data['time'] = visit.time.id
        serializer = VisitSerializer(visit, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        
        serialized_data = self.serializer_class(visit, data=data, partial=True)
        if serialized_data.is_valid():
            the_visit = serialized_data.update(instance=visit, validated_data=serialized_data.validated_data)
            return SuccessResponse(data=self.serializer_class(the_visit).data)



        #serializer = VisitSerializer(visit, data=data)
        if serializer.is_valid():
            serializer.update(instance=visit,validated_data=serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    '''


