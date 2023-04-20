from django.contrib import admin

from accounts.models import PetshopProfile

admin.site.register(PetshopProfile)

from product.models.pricing import ProductPricing

admin.site.register(ProductPricing)