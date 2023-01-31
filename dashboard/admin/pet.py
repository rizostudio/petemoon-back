from django.contrib import admin

from ..models import (Pet)


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    search_fields = ["name","user__first_name","user__phone_number"]
    list_display = ("name", "pet_type","pet_category","photo")


    