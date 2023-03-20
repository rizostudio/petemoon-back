from rest_framework import serializers
from accounts.models import VetProfile
from ..models import Visit
from django.db.models import Avg


class VisitSerializer(serializers.Serializer):
    
    pet = serializers.IntegerField()
    vet = serializers.IntegerField()
    explanation = serializers.CharField()
    reason = serializers.CharField(max_length=256)
    photo = serializers.ImageField()

    def create(self, validated_data):

        visit = Visit.objects.create(**validated_data)
        return visit
