from django.contrib import admin

from product.models import Picture


class PictureInline(admin.TabularInline):
    model = Picture
    extra = 0
