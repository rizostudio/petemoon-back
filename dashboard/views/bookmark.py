from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException
from dashboard.serializers import BookmarkSerializer
from dashboard.models import Bookmark, Product


class BookmarkView(APIView):

    serializer_class = BookmarkSerializer
    #authentication_classes = []
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookmark = Bookmark.objects.filter(user=request.user)
        result = self.serializer_class(bookmark, many=True).data
        return SuccessResponse(data=result)

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        try:
            if serialized_data.is_valid(raise_exception=True):
                product = Product.objects.get(
                    id=serialized_data.validated_data['product_id'])
                if Bookmark.objects.filter(user=request.user, product=product).exists():
                    raise CustomException(
                        detail=_("You added this product before"))
                serialized_data.save(user=request.user, product=product)
                return SuccessResponse(data={"message": _("bookmark added successfuly")})
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)

    def delete(self, request, id=None):
        try:
            try:
                Bookmark.objects.get(id=id).delete()
            except Bookmark.DoesNotExist:
                raise CustomException(detail=_("Bookmark does not exist"))

            return SuccessResponse(data={"message": _("Bookmark deleted successfuly")})

        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
