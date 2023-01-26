from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions


from config.responses import SuccessResponse, UnsuccessfulResponse
from product.models import ProductPricing
from ..serializers import ProductsSerializer

class PetShopProductsView(APIView):

    serializer_class = ProductsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = ProductPricing.objects.filter(petshop__owner__user=request.user)
        result = self.serializer_class(products,many=True).data
        return SuccessResponse(data=result)

    