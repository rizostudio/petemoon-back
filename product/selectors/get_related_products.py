from django.db.models import Avg, F, Max, Min, Q, Sum
from django.db.models.functions import Coalesce

from product.models import Product


def get_related_products(product: Product):
    return (
        Product.objects.filter(
            Q(category=product.category)
            | Q(pet_type=product.pet_type)
            | Q(brand=product.brand)
        )
        .exclude(id=product.id)
        .annotate(
            rating=Avg(
                "comments__rate",
                filter=Q(
                    comments__published=True, comments__product__slug=F("slug")
                ),
            )
        )
        .annotate(
            min_price=Min(
                Coalesce(
                    "productpricing__price_after_sale", "productpricing__price"
                ),
                filter=Q(
                    productpricing__inventory__gt=0,
                    productpricing__product=F("id"),
                ),
            )
        )
        .annotate(
            max_price=Max(
                "productpricing__price",
                filter=Q(
                    productpricing__inventory__gt=0,
                    productpricing__product=F("id"),
                ),
            )
        )
        .annotate(price=F("min_price"))
        .annotate(
            inventory=Sum(
                "productpricing__inventory",
                filter=Q(productpricing__product=F("id")),
            )
        )[:20]
    )
