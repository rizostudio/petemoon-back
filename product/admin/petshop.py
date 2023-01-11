from django.contrib import admin

from product.admin.pricing import PricingInline
from product.models import Petshop


@admin.register(Petshop)
class PetshopAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    inlines = [PricingInline]
    prepopulated_fields = {"slug": ("name",)}
