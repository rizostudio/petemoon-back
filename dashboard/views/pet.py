from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from dashboard.serializers import PetGeneralSerializer, PetMidicalSerializer
from dashboard.models import Pet


class PetViewSet(
        viewsets.GenericViewSet,
        mixins.UpdateModelMixin,
        mixins.CreateModelMixin):

    #serializer_class = PetSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        
        return Pet.objects.get(
            owner=self.request.user)

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

    @action(detail=False, methods=["get", "put"], url_path='pet-medical')
    def medical(self, request):

        if self.request.method == 'GET':
            # TODO this must be in new response format
            try:
                self.get_object()
            except Pet.DoesNotExist:
                return Response("Pet does not exists",status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(self.get_object())
            return Response(serializer.data)

        if self.request.method == 'PUT':
            serializer = self.get_serializer(
                self.get_object(), data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=False, methods=["get", "put"], url_path='pet-general')
    def general(self, request):

        if self.request.method == 'GET':
            # TODO this must be in new response format
            try:
                self.get_object()
            except Pet.DoesNotExist:
                return Response("Pet does not exists",status=status.HTTP_404_NOT_FOUND)

            serializer = self.get_serializer(self.get_object())
            return Response(serializer.data)


        if self.request.method == 'PUT':
            serializer = self.get_serializer(
                self.get_object(), data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
