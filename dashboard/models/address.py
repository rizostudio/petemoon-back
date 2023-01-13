from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Address(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    province = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    receiver = models.CharField(max_length=128)
    postal_code = models.CharField(max_length=10)
    postal_address = models.CharField(max_length=512)
    lat = models.DecimalField(_('Latitude'), max_digits=10, decimal_places=8, null=True)
    lon = models.DecimalField(_('Longitude'), max_digits=11, decimal_places=8, null=True)


    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
