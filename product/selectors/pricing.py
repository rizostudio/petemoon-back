from django.db import transaction

from product.models import ProductPricing


@transaction.atomic
def add_update_pricing(
    pet_shop_id: int, product_id: int, price: int, inventory: int
):
    ProductPricing.objects.update_or_create(
        product_id=product_id,
        petshop_id=pet_shop_id,
        defaults={
            "price": price,
            "inventory": inventory,
            "price_after_sale": None,
        },
    )
