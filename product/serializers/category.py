from rest_framework import serializers

from product.models import Category


class CategorySerializer(serializers.ModelSerializer):
    parent_catgory = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ("name", "slug", "parent_catgory")

    def get_parent_catgory(self, obj):
        return (
            CategorySerializer(obj.parent_category).data
            if obj.parent_category
            else None
        )
