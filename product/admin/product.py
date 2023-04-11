from django.contrib import admin

from product.admin.comment import CommentInline
from product.admin.picture import PictureInline
from product.admin.spec import SpecInline
from product.models import Product


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     search_fields = ["name"]
#     prepopulated_fields = {"slug": ("name",)}
#     list_display = ("name", "category", "pet_type", "brand")
#     inlines = [CommentInline, PictureInline, SpecInline]
admin.site.register(Product)