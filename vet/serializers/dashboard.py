from rest_framework import serializers



class PastVisitSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(source='user.first_name')
    time = serializers.DateTimeField(source='time.time')
    status = serializers.CharField()
    visit_id = serializers.CharField()
    pet_type = serializers.CharField(source='pet.pet_type')
    pet_category = serializers.CharField(source='pet.pet_category')
    phone_number = serializers.CharField(source='user.phone_number')
    pet_name = serializers.CharField(source='pet.name')
    explanation = serializers.CharField()
    reason = serializers.CharField()
    photo = serializers.FileField()
    prescription_photo = serializers.ImageField()
    prescription_summary = serializers.CharField()
    prescription = serializers.CharField()

        


class SinglePastVisitSerializer(serializers.Serializer):
    user_frist_name = serializers.CharField(source='user.first_name')
    time = serializers.DateTimeField(source='time.time')
    status = serializers.CharField()
    pet_type = serializers.CharField(source='pet.pet_type')
    phone_number = serializers.CharField(source='user.phone_number')
    pet_name = serializers.CharField(source='pet.name')
    prescription_photo = serializers.ImageField()
    prescription_summary = serializers.CharField()
    prescription = serializers.CharField()


class  FutureVisitSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(source='user.first_name')
    time = serializers.DateTimeField(source='time.time')
    status = serializers.CharField()
    visit_id = serializers.CharField()
    pet_type = serializers.CharField(source='pet.pet_type')
    pet_category = serializers.CharField(source='pet.pet_category')
    phone_number = serializers.CharField(source='user.phone_number')
    pet_name = serializers.CharField(source='pet.name')
    explanation = serializers.CharField()
    reason = serializers.CharField()
    photo = serializers.FileField()
    prescription_photo = serializers.ImageField()
    prescription_summary = serializers.CharField()
    prescription = serializers.CharField()
        

class SingleFutureVisitSerializer(serializers.Serializer):
    user_frist_name = serializers.CharField(source='user.first_name')
    time = serializers.DateTimeField(source='time.time')
    status = serializers.CharField()
    pet_type = serializers.CharField(source='pet.pet_type')
    pet_category = serializers.CharField(source='pet.pet_category')

    phone_number = serializers.CharField(source='user.phone_number')
    pet_name = serializers.CharField(source='pet.name')
    explanation = serializers.CharField()