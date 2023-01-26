from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions


from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException
from product.models import ProductPricing
from ..serializers import ProductsSerializer


class PetShopProductsView(APIView):

    serializer_class = ProductsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = ProductPricing.objects.filter(petshop__owner__user=request.user)
        result = self.serializer_class(products,many=True).data
        return SuccessResponse(data=result)

    def patch(self, request, id=None):
        serialized_data = self.serializer_class(request.user,data=request.data, partial=True)

        try:
            if serialized_data.is_valid(raise_exception=True):

                product_pricing = ProductPricing.objects.filter(petshop__owner__user=request.user,id=id)
                print(product_pricing)

                serialized_data.update(instance=product_pricing,validated_data=serialized_data.validated_data)

                return SuccessResponse(data={"message":_("product updated successfuly")})

        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)