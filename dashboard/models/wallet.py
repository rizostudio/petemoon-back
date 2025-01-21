from django.utils.translation import gettext_lazy as _
from django.db import models
from accounts.models.user import User


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    credit = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    charge = models.IntegerField(default=0)
    charge_ref_id = models.IntegerField(null=True, blank=True)
    
    class Meta:
        verbose_name = _("Wallet")
        verbose_name_plural = _("Wallets")

    def __str__(self):
        return str(self.user) +' | '+ str(self.credit)

