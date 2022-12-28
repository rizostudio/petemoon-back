from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import RegisterSerializer


class Register(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def patch(self, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        if user.is_registered:
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
            user.profile.save()
        return Response(
            {
                "success": True,
                "data": {"message": _("registeration completed")},
            },
            status=status.HTTP_200_OK,
        )
