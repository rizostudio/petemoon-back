from django.contrib import admin

from accounts.models import UserProfile, User
from .models import (Pet,Address, Bookmark,
                     Product, PetCategory, PetType, Message)

admin.site.register(Pet)
admin.site.register(Address)
admin.site.register(Bookmark)
admin.site.register(PetCategory)
admin.site.register(PetType)
admin.site.register(Message)
#TODO for test 
admin.site.register(UserProfile)
admin.site.register(User)
