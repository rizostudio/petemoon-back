from django.db import models

from accounts.models import PetshopProfile


class Petshop(models.Model):
    name = models.CharField(max_length=64)
    products = models.ManyToManyField(
        "product.Product", through="product.ProductPricing"
    )
    slug = models.SlugField(unique=True, db_index=True)
    owner = models.OneToOneField(
        PetshopProfile,
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="shops",
    )
