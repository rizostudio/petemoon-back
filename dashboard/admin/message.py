from django.contrib import admin

from ..models import (Message)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("title", "context","user")
    search_fields = ["user__first_name","user__phone_number"]



