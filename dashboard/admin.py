from django.contrib import admin
from .models import Pet, Order, Address, Favorite, Product

admin.site.register(Pet)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Favorite)
admin.site.register(Product)
