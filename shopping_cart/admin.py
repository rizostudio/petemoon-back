from django.contrib import admin
from .models import Order,PetShopOrder,Shipping
from dashboard.models import Wallet

admin.site.register(Order)
admin.site.register(Wallet)

admin.site.register(PetShopOrder)
admin.site.register(Shipping)

# Register your models here.
