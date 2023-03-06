from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.utils import timezone

from product.models import Product
from shopping_cart.models import Order

User = get_user_model()


def get_top_sales():
    last_month = timezone.now() - timedelta(days=30)
    last_month_orders = Order.objects.filter(created_at__gte=last_month)
    last_month_sales = (
        last_month_orders.values("products__product")
        .annotate(sell_count=Count("products__product"))
        .distinct()
        .order_by("-sell_count")[0:20]
    )
    last_month_sales_ids = [
        sale["products__product"] for sale in last_month_sales
    ]
    if len(last_month_sales_ids) < 20:
        remaining = 20 - len(last_month_sales_ids)
        return (
            Product.objects.filter(id__in=last_month_sales_ids)
            | Product.objects.exclued(id__in=last_month_sales_ids)[0:remaining]
        )
    return Product.objects.filter(id__in=last_month_sales_ids)


def get_recommended_products(user) -> list:
    """
    Returns list of recommended products for user
    """
    if user is None or user.is_anonymous:
        return get_top_sales()
    user_pets_types = user.pet_set.values_list("pet_type", flat=True)
    user_bought_products = (
        Order.objects.filter(user=user)
        .values("products__product")
        .annotate(sell_count=Count("products__product"))
        .distinct()
        .order_by("-sell_count")
    )
    bought_product_categories = (
        Product.objects.filter(id__in=user_bought_products)
        .values_list("category", flat=True)
        .distinct()
    )
    user_last_order_products = (
        Order.objects.filter(user=user)
        .order_by("-created_at")
        .values_list("products__product", flat=True)
    )
    recommended_products = (
        Product.objects.filter(
            pet_type__pet_type__in=user_pets_types,
            category__in=bought_product_categories,
        )
        .exclude(id__in=user_last_order_products)
        .distinct()
    )
    if recommended_products.count() < 20:
        remaining = 20 - recommended_products.count()
        return recommended_products | get_top_sales()[0:remaining]
    return recommended_products[0:20]
