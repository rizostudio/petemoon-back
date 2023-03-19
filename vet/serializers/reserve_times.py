from rest_framework import serializers

class PotentialTimeSerializer(serializers.Serializer):
    time = serializers.DateTimeField()

    
class AvailableTimeSerializer(serializers.Serializer):
    time = serializers.DateTimeField(read_only=True)
    available_time = serializers.ListField(write_only=True)