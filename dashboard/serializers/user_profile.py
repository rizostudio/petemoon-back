from rest_framework import serializers


class UserProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    phone_number = serializers.CharField(read_only=True)
    email = serializers.EmailField()
    birth_date = serializers.DateField(source="profile.birth_date")

    def update(self, instance, validated_data):
        user = instance
        if validated_data['email']:
            user.email = validated_data['email']
        if validated_data['profile']['birth_date']:
            user.profile.birth_date = validated_data['profile']['birth_date']
        user.save()
        user.profile.save()
        return user
