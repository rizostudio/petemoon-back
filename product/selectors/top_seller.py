from datetime import timedelta

from django.db.models import Count
from django.utils import timezone

from product.models import Petshop
from shopping_cart.models import Order


def get_top_seller():
    last_month = timezone.now() - timedelta(days=30)
    last_month_orders = Order.objects.filter(created_at__gte=last_month)
    last_month_sellers = (
        last_month_orders.values("products__petshop")
        .annotate(sell_count=Count("products__petshop"))
        .order_by("-sell_count")[0:3]
    )
    last_month_sellers_ids = [
        seller["products__petshop"] for seller in last_month_sellers
    ]
    if len(last_month_sellers_ids) < 3:
        remaining = 3 - len(last_month_sellers_ids)
        return (
            Petshop.objects.filter(id__in=last_month_sellers_ids)
            | Petshop.objects.all()[0:remaining]
        )
    return Petshop.objects.filter(id__in=last_month_sellers_ids)
