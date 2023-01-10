from django.contrib import admin

from product.models import ProductPricing


class PricingInline(admin.TabularInline):
    model = ProductPricing
    extra = 1
