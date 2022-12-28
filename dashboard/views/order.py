from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from dashboard.serializers import OrderSerializer
from dashboard.models import Order


class OrdersViewSet(viewsets.GenericViewSet,mixins.ListModelMixin,):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        
        return Order.objects.filter(
            user=self.request.user
        ) 

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
