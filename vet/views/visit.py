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
        serialized_data = self.serializer_class(data=request.data)
        try:
            if serialized_data.is_valid(raise_exception=True):
                serialized_data.save(user=request.user)
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


