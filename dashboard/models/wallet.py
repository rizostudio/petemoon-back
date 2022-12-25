from django.utils.translation import gettext_lazy as _
from django.db import models


class Wallet(models.Model):
    credit = models.FloatField()

    class Meta:
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallets")
