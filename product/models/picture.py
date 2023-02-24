from django.db import models
from django.utils.translation import gettext_lazy as _


class Picture(models.Model):
    image = models.ImageField(upload_to="product", verbose_name=_("Image"))
    product = models.ForeignKey(
        "product.Product", on_delete=models.CASCADE, related_name="pictures"
    )

    class Meta:
        verbose_name = _("Picture")
        verbose_name_plural = _("Pictures")
