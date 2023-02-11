import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.choices import Choices
from dashboard.models import Address
from product.models import ProductPricing


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    order_id = models.CharField(max_length=128,default=uuid.uuid4)
    status = models.CharField(choices=Choices.Order.choices, max_length=128)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    products = models.ManyToManyField(ProductPricing)
    total_price = models.IntegerField(null=True)
    shipping_method = models.CharField(max_length=128, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    @property
    def products_count(self):
        return self.products.count()

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return str(self.order_id)


class PetShopOrder(models.Model):
    user_order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(ProductPricing,on_delete=models.CASCADE)
    price = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        verbose_name = _("PetShopOrder")
        verbose_name_plural = _("PetShopOrders")


    # @receiver(post_save, sender=Order)
    # def create_petshop_order(sender, instance, created, **kwargs):
    #     print(instance.products.all())
    #     for product in instance.products.all():
    #         print(product)
