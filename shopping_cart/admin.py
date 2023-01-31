from django.contrib import admin
from .models import Order
from dashboard.models import Wallet

admin.site.register(Order)
admin.site.register(Wallet)
# Register your models here.
