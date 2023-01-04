from django.db.models import Avg, F, Min, Q
from django.db.models.functions import Coalesce

from product.models import Product


def get_item_by_slug(slug):
    return (
        Product.objects.filter(slug=slug)
        .annotate(
            rating=Avg(
                "comments__rate",
                filter=Q(
                    comments__published=True, comments__product__slug=F("slug")
                ),
            )
        )
        .annotate(
            price=Min(
                Coalesce(
                    "productpricing__price_after_sale", "productpricing__price"
                ),
                filter=Q(productpricing__inventory__gt=0),
            )
        )
        .prefetch_related("productpricing_set")
        .prefetch_related("comments")
        .prefetch_related("category")
        .first()
    )
