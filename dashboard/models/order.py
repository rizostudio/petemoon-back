from django.utils.translation import gettext_lazy as _
from django.db import models
from utils.choices import Choices
from django.contrib.auth.models import User
from . import Address


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=128)
    status = models.CharField(choices=Choices.Order.choices, max_length=128)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    price = models.FloatField()
    discount = models.FloatField()

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return self.order_id

