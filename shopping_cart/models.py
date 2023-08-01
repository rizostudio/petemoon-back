import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.choices import Choices
from dashboard.models import Address
from product.models import ProductPricing
from .utils import random_N_chars_str


class Shipping(models.Model):
    method = models.CharField(max_length=128)
    price = models.IntegerField()
    def __str__(self):
        return str(self.method) + ' | ' + str(self.price)

class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    order_id = models.CharField(max_length=128, unique=True,blank=True)
    status = models.CharField(choices=Choices.Order.choices, max_length=128)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    products = models.ManyToManyField(ProductPricing)
    total_price = models.IntegerField(null=True)
    shipping_method = models.ForeignKey(Shipping, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    @property
    def products_count(self):
        return self.products.count()

    def total_price_with_shipping(self):
        try:
            return self.shipping_method.price * self.total_price
        except:
            return None



    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return str(self.order_id)

    def save(self,*args, **kwargs):
        if not self.order_id:

            self.order_id = random_N_chars_str(12)
            # Generate ID once, then check the db. If exists, keep trying.
          
        super(Order, self).save()

class PetShopOrder(models.Model):
    user_order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(ProductPricing,on_delete=models.CASCADE)
    price = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True,editable=True,serialize=True)

    def __str__(self):
        return 'order_id:' + str(self.user_order.order_id) + ' - price:' + str(self.price)
    
    class Meta:
        verbose_name = _("PetShopOrder")
        verbose_name_plural = _("PetShopOrders")


    # @receiver(post_save, sender=Order)
    # def create_petshop_order(sender, instance, created, **kwargs):
    #     print(instance.products.all())
    #     for product in instance.products.all():
    #         print(product)
