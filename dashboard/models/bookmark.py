from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from product.models import Product


class Bookmark(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="bookmark_product")

    class Meta:
        verbose_name = _("Bookmark")
        verbose_name_plural = _("Bookmarks")

    def __str__(self):
        return self.product.name
