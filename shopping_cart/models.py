import uuid
from utils.choices import Choices
from dashboard.models import Address
from product.models import ProductPricing
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    order_id = models.CharField(max_length=128,default=uuid.uuid4)
    status = models.CharField(choices=Choices.Order.choices, max_length=128)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    products = models.ManyToManyField(ProductPricing)
    total_price = models.IntegerField(null=True)
    shipping_method = models.CharField(max_length=128, null=True)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return str(self.order_id)
