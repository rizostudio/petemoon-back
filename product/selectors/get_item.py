from django.db import connections
from django.db.models import Avg, F, Max, Min, Q, Sum
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
        .prefetch_related("brand")
        .prefetch_related("pet_type")
        .first()
    )


valid_orderings = {
    "cheapest": "price",
    "most_expensive": "-price",
}  # TODO expand this


def get_item_list(
    limit=16,
    offset=0,
    pet_types=None,
    category_slugs=None,
    max_price=None,
    min_price=None,
    brand_slugs=None,
    order_by=None,
    search=None,
):
    base = (
        Product.objects.annotate(
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
        )
    )
    if pet_types is not None and len(pet_types) > 0:
        base = base.filter(pet_type__slug__in=pet_types)
    if category_slugs is not None and len(category_slugs) > 0:
        base = base.filter(category__slug__in=category_slugs)
    if brand_slugs is not None and len(brand_slugs) > 0:
        base = base.filter(brand__slug__in=brand_slugs)
    if max_price is not None:
        base = base.filter(min_price__lte=max_price)
    if min_price is not None:
        base = base.filter(max_price__gte=min_price)
    if order_by in valid_orderings:
        base = base.order_by(valid_orderings[order_by])
    if (
        search is not None
        and len(search) > 0
        and connections["default"].vendor == "postgresql"
    ):
        from django.contrib.postgres.search import (
            SearchQuery,
            SearchRank,
            SearchVector,
        )

        vector = SearchVector("name", "details")
        query = SearchQuery(" ".join(search))
        base = base.annotate(rank=SearchRank(vector, query)).order_by("-rank")
    end = limit + offset
    total = base.count()
    return base[offset:end], total


def get_product_id_by_slug(product_slug):
    return (
        Product.objects.filter(slug=product_slug)
        .values_list("id", flat=True)
        .first()
    )
