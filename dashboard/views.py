from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from .serializers import (PetGeneralSerializer,PetMidicalSerializer,PetSerializer)
from .models import Pet



class AccountVeiwSet(viewsets.GenericViewSet):
    pass

class OrdersVeiwSet(viewsets.GenericViewSet):
    pass


class PetViewSet(
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin
):
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        
        return Pet.objects.get(
            owner=self.request.user
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def get_serializer_class(self):
        if self.action == 'medical':
            return PetMidicalSerializer
        if self.action == 'general':
            return PetGeneralSerializer
        
        return super().get_serializer_class()

    @action(detail=False, methods=["get","put"], url_path='medical')
    def medical(self, request):

        if self.request.method == 'GET':
            serializer = self.get_serializer(self.get_object())
            return Response(serializer.data)

        if self.request.method == 'PUT':
            serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path='general')
    def general(self, request):

        if self.request.method == 'GET':
            serializer = self.get_serializer(self.get_object())
            return Response(serializer.data)

        if self.request.method == 'PUT':
            serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
     