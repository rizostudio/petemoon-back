from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from dashboard.serializers import OrderSerializer
from dashboard.models import Order
from config.responses import SuccessResponse, UnsuccessfulResponse
from config.exceptions import CustomException
from dashboard.serializers import FavoriteSerializer
from dashboard.models import Favorite, Product


class FavoriteView(APIView):

    serializer_class = FavoriteSerializer
    #authentication_classes = []
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorite = Favorite.objects.filter(user=request.user)
        result = self.serializer_class(favorite, many=True).data
        return SuccessResponse(data=result)

    def post(self, request):
        serialized_data = self.serializer_class(data=request.data)
        try:
            if serialized_data.is_valid(raise_exception=True):
                product = Product.objects.get(
                    id=serialized_data.validated_data['product_id'])
                if Favorite.objects.filter(user=request.user, product=product).exists():
                    raise CustomException(
                        detail=_("You added this product before"))
                serialized_data.save(user=request.user, product=product)
                return SuccessResponse(data={"message": _("Favorite added successfuly")})
        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
        except exceptions.ValidationError as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)

    def delete(self, request, id=None):
        try:
            try:
                favorite = Favorite.objects.get(id=id).delete()
            except Favorite.DoesNotExist:
                raise CustomException(detail=_("Favorite does not exist"))

            return SuccessResponse(data={"message": _("Favorite deleted successfuly")})

        except CustomException as e:
            return UnsuccessfulResponse(errors=e.detail, status_code=e.status_code)
