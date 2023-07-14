from django.utils.translation import gettext as _
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from config.responses import bad_request, created, not_found
from product.serializers import CommentCreateSerialzer

from product.models import Product, ProductPricing
from shopping_cart.models import Order
from rest_framework.response import Response
from rest_framework import status


class CanComment(IsAuthenticated):
    def has_permission(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(slug=request.GET.get('slug'))
            product_pricing = ProductPricing.objects.filter(product=product)
            order_users = Order.objects.filter(products__in=product_pricing).values_list("user", flat=True).distinct()

            if request.user.id in order_users:
                return True
            else:
                return False
        except:
            return Response( {"success": False,"data": "you don't have permission or something wrong!",} ,status=status.HTTP_400_BAD_REQUEST, )




class CreateComment(APIView):
    permission_classes = [CanComment]

    def post(self, request, *args, **kwargs):
        product_slug = request.GET.get('slug')
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
