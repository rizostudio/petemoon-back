from rest_framework import serializers
from dashboard.models import Pet, PetType, PetCategory


class PetTypeSerializer(serializers.ModelSerializer):
        class Meta:
            model = PetType
            fields = "__all__"
         

class PetCategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = PetCategory
            fields = "__all__"
         

class PetGetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False)
    pet_type = PetTypeSerializer(required=False)
    sex = serializers.CharField(max_length=1)
    pet_category = PetCategorySerializer(required=False)
    birth_date = serializers.DateField(required=False)
    # medical
    weight = serializers.FloatField(required=False)
    last_vaccine_date = serializers.DateField(required=False)
    underlying_disease = serializers.CharField(required=False)
    last_anti_parasitic_vaccine_date = serializers.DateField(required=False)
    photo = serializers.ImageField(required=False)
    

    
class PetPostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    pet_type = serializers.IntegerField(required=False)
    sex = serializers.CharField(max_length=1)
    pet_category = serializers.IntegerField(required=False)
    birth_date = serializers.DateField()
    # medical
    weight = serializers.FloatField(required=False)
    last_vaccine_date = serializers.DateField(required=False)
    underlying_disease = serializers.CharField(required=False)
    last_anti_parasitic_vaccine_date = serializers.DateField(required=False)
    photo = serializers.ImageField(required=False,use_url=True)
    
    def create(self, validated_data):
        validated_data['pet_type'] = PetType.objects.get(
            id=validated_data['pet_type'])
        validated_data['pet_category'] = PetCategory.objects.get(
            id=validated_data['pet_category'])

        pet = Pet.objects.create(**validated_data)
        return pet

    def update(self, instance, validated_data):
        photo = validated_data.get('photo',None)
        print(photo)
        instance.update(**validated_data)

        return instance
