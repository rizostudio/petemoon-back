from django.utils.translation import gettext as _
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from config.responses import bad_request, created, not_found
from product.serializers import CommentCreateSerialzer


class CanComment(IsAuthenticated):
    pass


# TODO: create specific can comment permission


class CreateComment(APIView):
    permission_classes = [CanComment]

    def post(self, *args, **kwargs):
        product_slug = kwargs.get("slug")
        user = self.request.user
        data = self.request.data
        data["user"] = user.id
        data["product"] = product_slug
        serializer = CommentCreateSerialzer(data=data)
        if serializer.is_valid():
            serializer.save()
            return created(serializer.data)
        if "product" in serializer.errors:
            return not_found(errors=[_("Product not found.")])
        return bad_request(errors=serializer.errors)
