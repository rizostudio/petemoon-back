from django.utils.translation import gettext as _
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from config.responses import bad_request, created, not_found
from vet.serializers import VetCommentSerializer
from vet.models import VetComment
from rest_framework.response import Response
from rest_framework import status
from accounts.models import VetProfile
from config.responses import SuccessResponse, UnsuccessfulResponse


class CreateComment(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VetCommentSerializer

    def post(self, request, *args, **kwargs):
        vet_id = kwargs.get("id")
        user = self.request.user
        data = self.request.data
        data["user"] = 11
        data["vet"] = vet_id
        serializer = VetCommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return created(serializer.data)
        if "vet" in serializer.errors:
            return not_found(errors=[_("Product not found.")])
        return bad_request(errors=serializer.errors)



class Comments(APIView):
    serializer_class = VetCommentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        vet_profile = VetProfile.objects.get(user=request.user)
        comments = VetComment.objects.filter(vet=vet_profile)
        comments_serializer = VetCommentSerializer(comments, many=True)
        return SuccessResponse(data=comments_serializer.data)

