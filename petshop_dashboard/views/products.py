from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException
from product.models import ProductPricing
from petshop_dashboard.serializers import PetShopProductPricingSerializer
from product.serializers import ProductListSerializer
from product.models import Petshop

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
                    
                    product_pricing = ProductPricing.objects.filter(
                        product__id=serialized_data.validated_data["product_id"],
                        petshop__owner__user=request.user)
                    if product_pricing.exists():
                        raise CustomException(detail="You created this product before")
                    
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

    def get(self, *args, **kwargs):
        query_params = self.request.query_params
        # Start with all products
        products = Product.objects.annotate(
            rating=Avg(
                "comments__rate",
                filter=Q(
                    comments__published=True, comments__product__slug=F("slug")
                ),
            )
        ).annotate(
            min_price=Min(
                Coalesce(
                    "productpricing__price_after_sale", "productpricing__price"
                ),
                filter=Q(
                    productpricing__inventory__gt=0,
                    productpricing__product=F("id"),
                ),
            )
        ).annotate(
            max_price=Max(
                "productpricing__price",
                filter=Q(
                    productpricing__inventory__gt=0,
                    productpricing__product=F("id"),
                ),
            )
        ).annotate(
            inventory=Sum(
                "productpricing__inventory",
                filter=Q(productpricing__product=F("id")),
            )
        )
        
        pet_types = query_params.get("pet_types", "").split(",")
        if pet_types != ['']:
            products = products.filter(pet_type__slug__in=pet_types)

        # Filter by pet categories
        pet_categories = query_params.get("pet_categories", "").split(",")
        if pet_categories != ['']:
            products = products.filter(category__slug__in=pet_categories)


        # # Filter by brand slugs
        brand_slugs = query_params.get("brand_slugs", "").split(",")
        if brand_slugs != ['']:
            products = products.filter(brand__slug__in=brand_slugs)

        # Filter by price range
        max_price = query_params.get("max_price",None)
        min_price = int(query_params.get("min_price","0"))
        
        if max_price is not None:
            products = products.filter(max_price__lte=int(max_price))
        if min_price is not None:
            products = products.filter(min_price__gte=min_price)

        # Order the results
        order_by = query_params.get("order_by")
        if order_by == "name":
            products = products.order_by("name")
        elif order_by == "min_price":
            products = products.order_by("min_price")
        elif order_by == "max_price":
            products = products.order_by("max_price")
        elif order_by == "popular":
            products = products.order_by("rate")
        elif order_by == "newest":
            products = products.order_by("productpricing__created_at")


        # Apply limit and offset
        limit = int(query_params.get("limit", "16"))
        offset = int(query_params.get("offset", "0"))
        products = products[offset:offset+limit]

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