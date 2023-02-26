from django.contrib import admin

from product.models import Spec


class SpecInline(admin.TabularInline):
    model = Spec
    extra = 0
