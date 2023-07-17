from rest_framework.views import APIView

from config.responses import ok
from product.selectors import get_recommended_products
from product.serializers import ProductListSerializer, ProductGetSerializer

class GetRecommended(APIView):
    def get(self, *args, **kwargs):
        user = self.request.user
        products = get_recommended_products(user)
        return ok(data=ProductGetSerializer(products, many=True).data)



