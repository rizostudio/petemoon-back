from django.utils.translation import gettext_lazy as _
from django.db import models
from utils.choices import Choices
from django.contrib.auth.models import User


class Pet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    type = models.PositiveSmallIntegerField(choices=Choices.PetType.choices)
    sex = models.CharField(choices=Choices.Sex.choices,max_length=1)
    species = models.CharField(max_length=128)
    birth_date = models.DateField(null=True)

    #Medical
    weight = models.FloatField()
    last_vaccine_date = models.DateField(null=True)
    underlying_disease = models.CharField(max_length=128,null=True)
    last_anti_parasitic_vaccine_date = models.DateField(null=True)

    class Meta:
        verbose_name = _("Pet")
        verbose_name_plural = _("Pets")

    def __str__(self):
        return self.name


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

 

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order_id = models.CharField(max_length=128)
    status = models.CharField(choices=Choices.Order.choices,max_length=128)
    address = models.ForeignKey(Address,on_delete=models.SET_NULL,null=True)
    price = models.FloatField()
    discount = models.FloatField()

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return self.order_id
