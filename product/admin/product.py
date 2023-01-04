from django.contrib import admin

from product.admin.comment import CommentInline
from product.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "category", "animal_type", "brand")
    inlines = [CommentInline]
