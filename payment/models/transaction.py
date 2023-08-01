from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from shopping_cart.models import Order


class Transaction(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name="transactions")
    amount = models.IntegerField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    transaction_type_choices = (
        ("wallet", _("wallet")),
        ("order", _("order")),
        ("vet", _("vet")),
    )
    transaction_type = models.CharField(choices=transaction_type_choices, max_length=8)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, null=True, blank=True)
    authority = models.CharField(max_length=36, null=True, blank=True)
    ref_id = models.IntegerField(null=True, blank=True)
    success = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"{self.description}-{self.amount}-{self.user}"
            f"-{self.ref_id}-{self.success}"
        )




class PetshopSaleFee(models.Model):
    percent = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.percent)