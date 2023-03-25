from rest_framework import serializers
from ..models import VetComment



class VetCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = VetComment
        fields = ("user", "title", "text", "rate", "created_at")
