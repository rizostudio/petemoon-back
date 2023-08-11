from rest_framework import serializers
from dashboard.models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['title', 'context', 'created']

