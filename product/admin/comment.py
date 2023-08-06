from django.contrib import admin

from product.models import Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ("user", "title", "text", "rate", "created_at")

    def has_add_permission(self, *args, **kwargs):
        return False




class CommentAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "title")
admin.site.register(Comment, CommentAdmin)
