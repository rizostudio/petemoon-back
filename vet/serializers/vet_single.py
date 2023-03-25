from rest_framework import serializers
from accounts.models import VetProfile
from ..models import VetComment
from django.db.models import Avg
from . import AvailableTimeSerializer
from .comments import VetCommentSerializer

class VetSingleSerializer(serializers.Serializer):
    
    photo = serializers.ImageField()
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    average_rating = serializers.SerializerMethodField(read_only=True)
    about = serializers.CharField()
    comments_count = serializers.SerializerMethodField(read_only=True)
    reserve_times = AvailableTimeSerializer(many=True)
    comments = serializers.SerializerMethodField(read_only=True)


    def get_average_rating(self, obj):
        print(obj)
        return VetComment.objects.filter(vet=obj).aggregate(
            avg_rating=Avg("rate")
        )["avg_rating"]
    
    def get_comments_count(self, obj):
        return VetComment.objects.filter(vet=obj).count()

    def get_comments(self, obj):
        return VetCommentSerializer(VetComment.objects.filter(vet=obj),many=True).data



# class CommentCreateSerialzer(serializers.ModelSerializer):
#     product = serializers.SlugRelatedField(
#         slug_field="slug", write_only=True, queryset=Product.objects.all()
#     )

#     class Meta:
#         model = VetComment
#         fields = ("user", "product", "title", "text", "rate")
#         extra_kwargs = {"user": {"write_only": True}}
