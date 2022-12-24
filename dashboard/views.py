from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import (
    PetGeneralSerializer,PetMidicalSerializer,PetSerializer,AddressSerializer,ProfileSerializer)
from .models import Pet,Address



class ProfileViewSet(viewsets.GenericViewSet):

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
        
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self):
        serializer = self.get_serializer(data=self.request.user)
        return Response(serializer.data)


class OrdersViewSet(viewsets.GenericViewSet):
    pass

class AddressViewSet(
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin):

    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        
        return Address.objects.filter(
            user=self.request.user
        )


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

   

class PetViewSet(
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin):

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

    @action(detail=False, methods=["get","put"], url_path='pet-medical')
    def medical(self, request):

        if self.request.method == 'GET':
            serializer = self.get_serializer(self.get_object())
            return Response(serializer.data)

        if self.request.method == 'PUT':
            serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=False, methods=["get","put"], url_path='pet-general')
    def general(self, request):

        if self.request.method == 'GET':
            serializer = self.get_serializer(self.get_object())
            return Response(serializer.data)

        if self.request.method == 'PUT':
            serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
     