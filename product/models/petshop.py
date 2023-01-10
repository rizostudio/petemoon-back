from django.db import models


class Petshop(models.Model):
    name = models.CharField(max_length=64)
    products = models.ManyToManyField(
        "product.Product", through="product.ProductPricing"
    )
    slug = models.SlugField(unique=True, db_index=True)
