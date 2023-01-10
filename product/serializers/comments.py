from rest_framework import serializers

from product.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ("user", "title", "text", "rate", "created_at")
