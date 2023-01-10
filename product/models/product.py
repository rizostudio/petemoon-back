from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True)
    category = models.ForeignKey(
        "product.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        to_field="name",
    )
    animal_type_choice = (
        ("cats", "Cats"),
        ("dogs", "Dogs"),
        ("birds", "Birds"),
        ("reptiles", "Reptiles"),
        ("fish", "Fish"),
        ("rodents", "Rodents"),
        ("other", "Other"),
    )
    animal_type = models.CharField(
        max_length=8, choices=animal_type_choice, default="other"
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
            return f"{self.brand__name}-{self.name}-{self.category_name}"
        else:
            return f"{self.brand__name}-{self.name}"
