from django.contrib import admin
from .models import User, PetshopProfile, VetProfile

admin.site.register(User)
admin.site.register(PetshopProfile)
admin.site.register(VetProfile)