from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException

from .utils import add_to_cart

class CartView(APIView):

    #serializer_class = BookmarkSerializer
    #authentication_classes = []
    #permission_classes = [IsAuthenticated]

    def get(self, request):
        add_to_cart(1,"liji",3)
        add_to_cart(1,"lighuo",2)
        return SuccessResponse(data="result")

    # def post(self, request):
    #     serialized_data = self.serializer_class(data=request.data)
    #     try:
    #         if serialized_data.is_valid(raise_exception=True):
    #             product = Product.objects.get(
    #                 id=serialized_data.validated_data['product_id'])
    #             if Bookmark.objects.filter(user=request.user, product=product).exists():
    #                 raise CustomException(
    #                     detail=_("You added this product before"))
    #             serialized_data.save(user=request.user, product=product)
    #             return SuccessResponse(data={"message": _("bookmark added successfuly")})
    #     except CustomException as e:
    #         return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
    #     except exceptions.ValidationError as e:
    #         return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)