from django.utils.translation import gettext as _
from rest_framework.views import APIView

from accounts.functions import expire
from config.responses import ok


class Logout(APIView):
    def get(self, *args, **kwargs):
        access_from_cookie = self.request.COOKIES.get(
            "HTTP_ACCESS"
        ) or self.request.COOKIES.get("HTTP_AUTHORIZATION")
        access_from_header = self.request.META.get(
            "HTTP_ACCESS"
        ) or self.request.META.get("HTTP_AUTHORIZATION")
        access = access_from_cookie or access_from_header
        if access is not None:
            expire(access)
        response = ok({"message": _("Logged out")})
        response.delete_cookie.set_cookie(
            "HTTP_ACCESS",
            "",
            max_age=0,
            secure=True,
            httponly=True,
            samesite="None",
        )
        return response
