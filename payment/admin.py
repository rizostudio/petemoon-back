from django.contrib import admin
from .models import Transaction, PetshopSaleFee, Discount


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('code', 'active', 'creator', 'percentage', 'created_at')
    readonly_fields = ('code',)
admin.site.register(Discount, DiscountAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'created_at', 'success')
admin.site.register(Transaction, TransactionAdmin)

admin.site.register(PetshopSaleFee)