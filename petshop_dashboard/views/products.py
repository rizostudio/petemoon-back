from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException
from product.models import ProductPricing
from ..serializers import ProductPricingSerializer
from product.serializers import ProductListSerializer
from product.selectors import get_item_list
from product.models import Petshop


class PetShopProductPricingView(APIView):

    serializer_class = ProductPricingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = ProductPricing.objects.filter(
            petshop__owner__user=request.user)
        result = self.serializer_class(products, many=True).data
        return SuccessResponse(data=result)

    def patch(self, request, id=None):
        serialized_data = self.serializer_class(
            request.user, data=request.data, partial=True)

        try:
            if serialized_data.is_valid(raise_exception=True):

                product_pricing = ProductPricing.objects.filter(
                    petshop__owner__user=request.user, id=id)

                serialized_data.update(
                    instance=product_pricing, validated_data=serialized_data.validated_data)

                return SuccessResponse(data={"message": _("product updated successfuly")})

        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        petshop = Petshop.objects.get(owner__user=request.user)
        try:
            if serialized_data.is_valid(raise_exception=True):
                try:
                    from product.models import Product
                    serialized_data.validated_data["product"] = Product.objects.get(id=serialized_data.validated_data["product_id"])
                    product_pricing = ProductPricing.objects.create(serialized_data.validated_data)
                except CustomException :
                    raise CustomException(detail="IUHUIOG")
            return SuccessResponse(data={"message":_("Product pricing added successfuly")})
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)

class ProductsView(APIView):

    serializer_class = ProductListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query_params = self.request.query_params
        try:
            kw = {
                "limit": int(query_params.get("limit", "16")),
                "offset": int(query_params.get("limit", "0")),
                "pet_types": query_params.get("pet_types", "").split(","),
                "category_slugs": query_params.get("category_slugs", "").split(
                    ","
                ),
                "brand_slugs": query_params.get("brand_slugs", "").split(","),
                "max_price": int(query_params.get("max_price", None)),
                "min_price": int(query_params.get("min_price", None)),
                "order_by": query_params.get("order_by"),
                "search": query_params.get("search", "").split("+"),
            }
        except CustomException:
            kw = {}
        try:
            items, count = get_item_list(**kw)
        except CustomException as e:
            raise e
        return SuccessResponse({"products": self.serializer_class(items, many=True).data, "count": count, })
