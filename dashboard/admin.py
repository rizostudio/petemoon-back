from django.contrib import admin
from .models import (Pet, Order, Address, Bookmark,
                     Product, PetCategory, PetType, Message)

admin.site.register(Pet)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(Bookmark)
admin.site.register(Product)
admin.site.register(PetCategory)
admin.site.register(PetType)
admin.site.register(Message)
