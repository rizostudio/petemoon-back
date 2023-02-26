from django.db import models
from django.utils.translation import gettext_lazy as _


class Spec(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Name"))
    value = models.CharField(max_length=100, verbose_name=_("Value"))
    product = models.ForeignKey(
        "product.Product", on_delete=models.CASCADE, related_name="specs"
    )

    class Meta:
        verbose_name = _("Spec")
        verbose_name_plural = _("Specs")

    def __str__(self):
        return self.name
