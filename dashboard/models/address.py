from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import User


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    province = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    receiver = models.CharField(max_length=128)
    postal_code = models.CharField(max_length=10)
    postal_address = models.CharField(max_length=512)

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
