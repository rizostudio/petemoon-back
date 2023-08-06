from django.contrib import admin
from .models import Transaction, PetshopSaleFee


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'created_at', 'success')
admin.site.register(Transaction, TransactionAdmin)

admin.site.register(PetshopSaleFee)