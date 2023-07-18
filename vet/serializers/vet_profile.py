from rest_framework import serializers
from accounts.models import VetProfile
from dashboard.serializers import UserProfileSerializer


class VetProfileSerialzer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    class Meta:
        model = VetProfile
        fields = "__all__"
