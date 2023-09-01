from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.functions import get_user_data
from accounts.serializers import RegisterSerializer


class Register(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def patch(self, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        if user.register_completed:
            return Response(
                {
                    "success": False,
                    "errors": [_("user is already registered")],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = RegisterSerializer(user, data=data, partial=True)
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "errors": [_("incorrect data"), serializer.errors],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save()
        if hasattr(user, "profile") and "referal_code" in data:
            user.profile.referal_code = data["referal_code"]
            user.first_name = data["first_name"]
            user.last_name = data["last_name"]
            user.profile.first_name = data["first_name"]
            user.profile.last_name = data["last_name"]
            user.save()
            user.profile.save()
        user.refresh_from_db()
        user_data = get_user_data(user)
        user.register_completed = True
        user.save()
        return Response(
            {
                "success": True,
                "data": {"user_data": user_data},
            },
            status=status.HTTP_200_OK,
        )
