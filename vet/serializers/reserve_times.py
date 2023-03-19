from rest_framework import serializers

class PotentialTimeSerializer(serializers.Serializer):
    time = serializers.DateTimeField()

    