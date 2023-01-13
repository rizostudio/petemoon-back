from django.db import models

from dashboard.models import PetCategory


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True)
    category = models.ForeignKey(
        "product.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        to_field="name",
    )
    pet_type = models.ForeignKey(
        PetCategory, on_delete=models.SET_NULL, null=True
    )
    picture = models.ImageField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    specs = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, db_index=True)

    brand = models.ForeignKey(
        "product.Brand", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        if self.category is not None:
            return f"{self.brand.name}-{self.name}-{self.category.name}"
        else:
            return f"{self.brand.name}-{self.name}"
