from rest_framework import serializers
from accounts.models import VetProfile
from ..models import Visit
from django.db.models import Avg
from dashboard.models import Pet
from accounts.models import User
from ..models import ReserveTimes
from django.db import transaction


class VisitSerializer(serializers.Serializer):

    pet = serializers.IntegerField()
    vet = serializers.IntegerField()
    explanation = serializers.CharField()
    reason = serializers.CharField(max_length=256)
    photo = serializers.FileField(required=False)
    prescription_photo = serializers.FileField(required=False)
    time = serializers.IntegerField()

    @transaction.atomic
    def create(self, validated_data):
        validated_data['pet'] = Pet.objects.get(id=validated_data['pet'])
        validated_data['vet'] = User.objects.get(id=validated_data['vet'])
        reserve_time = ReserveTimes.objects.get(id=validated_data.pop("time"))
        reserve_time.reserved=True
        reserve_time.save()
        visit = Visit.objects.create(**validated_data)
        return visit


    def update(self, instance, validated_data):
        visit = instance
        if validated_data['explanation']:
            visit.explanation = validated_data['explanation']
        if validated_data['reason']:
            visit.reason = validated_data['reason']
        if validated_data['prescription_photo']:
            visit.prescription_photo = validated_data['prescription_photo']
        visit.save()
        return visit


