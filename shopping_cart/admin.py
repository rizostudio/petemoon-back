from django.contrib import admin
from .models import Order,PetShopOrder,Shipping
from dashboard.models import Wallet

admin.site.register(Order)
admin.site.register(Wallet)

admin.site.register(Shipping)

@admin.register(PetShopOrder)
class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', )