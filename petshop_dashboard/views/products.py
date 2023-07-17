from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException
from product.models import ProductPricing
from petshop_dashboard.serializers import PetShopProductPricingSerializer
from product.serializers import ProductListSerializer
from product.models import Petshop, Product

from config.responses import ok
from product.serializers import ProductGetSerializer
from product.models import Product

from django.db.models import Avg, F, Max, Min, Q, Sum
from django.db.models.functions import Coalesce


class PetShopProductPricingView(APIView):

    serializer_class = PetShopProductPricingSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query_params = self.request.query_params
       
        if query_params.get("pet_type")!= None:
            products = ProductPricing.objects.filter(
                petshop__owner__user=request.user,
                product__pet_type__slug=query_params.get("pet_type"))
        else:
            products = ProductPricing.objects.filter(
                petshop__owner__user=request.user)

        if query_params.get("newest") == "True":
            products = products.order_by("-created_at")


        order_by = query_params.get("order_by")
        
        if order_by == "low_price":
            products = products.order_by("price")
        elif order_by == "high_price":
            products = products.order_by("-price")


        result = self.serializer_class(products, many=True).data
        return SuccessResponse(data=result)

    def patch(self, request, id=None):
        serialized_data = self.serializer_class(request.user, data=request.data, partial=True)

        try:
            if serialized_data.is_valid(raise_exception=True):

                product_pricing = ProductPricing.objects.filter(
                    petshop__owner__user=request.user, id=id)

                serialized_data.update(
                    instance=product_pricing, validated_data=serialized_data.validated_data)

                return ok(data={"message": _("product updated successfuly")})

        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        petshop = Petshop.objects.get(owner__user=request.user)
        try:
            if serialized_data.is_valid(raise_exception=True):
                    product_pricing = ProductPricing.objects.filter(
                        product__id=serialized_data.validated_data["product_id"],
                        petshop__owner__user=request.user)
                    if product_pricing.exists():
                        raise CustomException(detail="You added this product before")
                    
                    serialized_data.save(petshop=petshop)
            return SuccessResponse(data={"message":_("Product pricing added successfuly")})
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)


    def delete(self, request, id=None):
        try:
            try:
                pricing = ProductPricing.objects.get(id=id,petshop__owner__user=request.user).delete()
            except ProductPricing.DoesNotExist:
                raise CustomException(detail=_("Product pricing does not exist"))

            return SuccessResponse(data={"message":_("product pricing deleted successfuly")})
                
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code) 


class ProductsView(APIView):

    serializer_class = ProductListSerializer
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()

    def get(self, *args, **kwargs):
        query_params = self.request.query_params
        products = self.queryset.all() 

        # Filter by pet types
        pet_types = query_params.get("pet_types", "").split(",")
        if pet_types != ['']:
            products = self.queryset.filter(pet_type__slug__in=pet_types)

        
        # Filter by pet categories
        pet_category = query_params.get("pet_category", "").split(",")
        if pet_category != ['']:
            products = self.queryset.filter(category__slug__in=pet_category)


        # # Filter by brand slugs
        brand = query_params.get("brand", "").split(",")
        if brand != ['']:
            products = self.queryset.filter(brand__slug__in=brand)


    #     # Order the results
    #     order_by = query_params.get("order_by")
    #     if order_by == "name":
    #         products = products.order_by("name")
    #     elif order_by == "newest":
    #         products = products.order_by("productpricing__created_at")


    #     # Apply limit and offset
    #     limit = int(query_params.get("limit", "16"))
    #     offset = int(query_params.get("offset", "0"))
    #     products = products[offset:offset+limit]

        # If no products are found, raise a 404 exception
  
        return ok(
            {"products": ProductGetSerializer(products, many=True).data,
             "count": products.count()}
             )



class SingleProductPricingView(APIView):
    serializer_class = PetShopProductPricingSerializer

    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
           
        pricing = ProductPricing.objects.get(id=id)
        result = self.serializer_class(pricing).data
        return SuccessResponse(data=result)
    


class SingleProductView(APIView):
    serializer_class = ProductGetSerializer

    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
           
        product = Product.objects.get(id=id)
        result = self.serializer_class(product).data
        return SuccessResponse(data=result)