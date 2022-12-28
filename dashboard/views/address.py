from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from dashboard.serializers import AddressSerializer
from dashboard.models import Address


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
