from django.db.models import F, Max, Min
from django.db.models.functions import Coalesce
from rest_framework.views import APIView

from config.responses import ok
from dashboard.models import PetCategory
from product.models import Brand, ProductPricing
from utils.choices import Choices


class GetFilters(APIView):
    def get(self, request):
        brands = Brand.objects.all().values("name", "slug")
        categories = PetCategory.objects.all().values("name", "slug")
        pet_types = (
            PetCategory.objects.all()
            .annotate(name=F("pet_category"))
            .values("name", "slug")
        )
        max_price = ProductPricing.objects.filter(inventory__gt=0).aggregate(
            Max("price")
        )["price__max"]
        min_price = ProductPricing.objects.filter(inventory__gt=0).aggregate(
            min_price=Min(
                Coalesce("price_after_sale", "price"),
            )
        )["min_price"]
        pet_categories = [
            {"id": i[0], "name": i[1]} for i in Choices.PetType.choices
        ]
        data = {
            "brands": brands,
            "categories": categories,
            "pet_types": pet_types,
            "max_price": max_price,
            "min_price": min_price,
            "pet_categories": pet_categories,
        }
        return ok(data)
