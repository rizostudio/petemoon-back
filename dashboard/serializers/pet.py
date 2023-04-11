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
        instance.name = validated_data.get('name', instance.name)
        instance.pet_type = validated_data.get('pet_type', instance.pet_type)
        instance.sex = validated_data.get('sex', instance.sex)
        instance.pet_category = validated_data.get('pet_category', instance.pet_category)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.last_vaccine_date = validated_data.get('last_vaccine_date', instance.last_vaccine_date)
        instance.underlying_disease = validated_data.get('underlying_disease', instance.underlying_disease)
        instance.last_anti_parasitic_vaccine_date = validated_data.get(
             'last_anti_parasitic_vaccine_date', instance.last_anti_parasitic_vaccine_date)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.save()

        return instance