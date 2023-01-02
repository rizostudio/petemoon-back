from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, db_index=True)
    parent_category = models.ForeignKey(
        "product.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        to_field="name",
    )

    def __str__(self):
        if self.parent_category is not None:
            return f"{self.name}-{self.parent_category_name}"
        else:
            return self.name
