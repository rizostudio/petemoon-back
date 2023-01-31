from django.contrib import admin

from ..models import (PetCategory)


@admin.register(PetCategory)
class PetCategoryAdmin(admin.ModelAdmin):
    search_fields = ["pet_category"]

    