from django.contrib.auth import get_user_model
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("email", "first_name", "last_name")
        extra_kwargs = {
            "email": {"required": False},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }
