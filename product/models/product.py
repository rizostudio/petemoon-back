from django.db import models
from django.utils.text import slugify
from dashboard.models import PetCategory, PetType


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True)
    category = models.ForeignKey(
        PetCategory,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    pet_type = models.ForeignKey(
        PetType, on_delete=models.SET_NULL, null=True
    )
    picture = models.ImageField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    slug = models.CharField(unique=True, db_index=True, max_length=256)

    brand = models.ForeignKey(
        "product.Brand", on_delete=models.SET_NULL, null=True
    )
    specific = models.CharField(max_length=128, null=True, blank=True)
    size = models.CharField(max_length=256, null=True, blank=True)
    weight =  models.IntegerField(null=True, blank=True)
    made_in = models.CharField(max_length=256, null=True, blank=True)
    other_details = models.TextField( null=True, blank=True)
    
    def __str__(self):
        if self.category is not None:
            return f"{self.brand.name}-{self.name}-{self.category.pet_category}"
        else:
            return f"{self.brand.name}--{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name, allow_unicode=True)
        super(Product, self).save(*args, **kwargs)