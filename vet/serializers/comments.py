from rest_framework import serializers
from ..models import VetComment



class VetCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VetComment
        fields = ("vet" ,"user", "title", "text", "rate", "created_at")
