from rest_framework.views import APIView

from config.responses import ok
from product.selectors import get_item_list
from product.serializers import ProductGetSerializer
from ..models import Product

from django.db.models import Avg, F, Max, Min, Q, Sum
from django.db.models.functions import Coalesce

class GetList(APIView):
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
        print(pet_types)
        if pet_types != ['']:
            products = products.filter(pet_type__slug__in=pet_types)

        # Filter by pet categories
        pet_categories = [x for x in query_params.get("pet_categories", "").split(",") if x]
        if pet_categories:
            pet_category_ids = [int(x) for x in pet_categories]
            products = products.filter(category__in=pet_category_ids)


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


