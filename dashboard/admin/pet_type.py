from django.contrib import admin

from ..models import (PetType)


@admin.register(PetType)
class PetTAdmin(admin.ModelAdmin):
    search_fields = ["pet_type"]

    