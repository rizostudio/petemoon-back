from django.contrib import admin
from .models import Order,PetShopOrder,Shipping
from dashboard.models import Wallet


admin.site.register(Wallet)
admin.site.register(Shipping)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'status', 'total_price_with_shipping', 'created_at')
admin.site.register(Order, OrderAdmin)

#@admin.register(PetShopOrder)
class PetShopOrderAdmin(admin.ModelAdmin):
    list_display = ('user_order', 'price', 'price_with_shipping_and_fee', 'created_at' )
    readonly_fields = ('created_at',)
admin.site.register(PetShopOrder, PetShopOrderAdmin)