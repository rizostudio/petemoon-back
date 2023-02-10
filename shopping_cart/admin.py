from django.contrib import admin
from .models import Order,PetShopOrder
from dashboard.models import Wallet

admin.site.register(Order)
admin.site.register(Wallet)

admin.site.register(PetShopOrder)
# Register your models here.
