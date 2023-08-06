from rest_framework import serializers
from accounts.serializers import UserSerializer
from product.models import Comment, Product


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    #user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ("user", "title", "text", "rate", "created_at")


class CommentCreateSerialzer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field="slug", write_only=True, queryset=Product.objects.all())

    class Meta:
        model = Comment
        fields = ("user", "product", "title", "text", "rate")
        extra_kwargs = {"user": {"write_only": True}}
