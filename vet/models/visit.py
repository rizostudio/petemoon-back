from django.db import models
from django.contrib.auth import get_user_model
from shopping_cart.utils import random_N_chars_str
from utils.choices import Choices
from .reserve_times import ReserveTimes
from accounts.models import User

class Visit(models.Model):
    vet = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="visit_vet")
    visit_id = models.CharField(max_length=128,unique=True,editable=False,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True, related_name="visit_user" )
    pet = models.ForeignKey("dashboard.Pet",on_delete=models.CASCADE,null=True,blank=True)
    explanation = models.TextField()
    reason = models.CharField(max_length=256)
    photo = models.ImageField(blank=True,null=True)
    time = models.ForeignKey(ReserveTimes,on_delete=models.CASCADE, null=True )
    prescription_summary = models.CharField(max_length=256,null=True,blank=True)
    prescription = models.TextField(blank=True)
    prescription_photo = models.ImageField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    status = models.CharField(choices=Choices.Visit.choices, default="PENDING", max_length=128, null=True,blank=True)
    authority = models.CharField(max_length=36, null=True, blank=True)
    ref_id = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(default=200)

    def save(self):
        self.visit_id = default=random_N_chars_str(12)          
        super(Visit, self).save()



''' 

class VisitOrder(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    order_id = models.CharField(max_length=128, unique=True, blank=True)
    status = models.CharField(choices=Choices.Order.choices, max_length=128)
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    total_price = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = _("VisitOrder")
        verbose_name_plural = _("VisitOrders")

    def __str__(self):
        return str(self.order_id)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = random_N_chars_str(12)
        super(VisitOrder, self).save()




class VetVisitOrder(models.Model):
    user_order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(ProductPricing, on_delete=models.CASCADE)
    price = models.IntegerField(null=True)
    price_with_shipping_and_fee = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, editable=True, serialize=True)

    def save(self, *args, **kwargs):
        if not self.price_with_shipping_and_fee:
            self.price_with_shipping_and_fee = self.user_order.shipping_method.price + (
                        self.price - ((self.price * fee()) / 100))
        super(PetShopOrder, self).save(*args, **kwargs)

    def __str__(self):
        return 'order_id:' + str(self.user_order.order_id) + ' - price:' + str(self.price)

'''