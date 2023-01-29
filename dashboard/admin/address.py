from django.contrib import admin

from ..models import (Address)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    search_fields = ["receiver","postal_code"]


