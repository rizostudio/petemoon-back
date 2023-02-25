from rest_framework.views import APIView

from config.responses import ok
from product.selectors import get_on_sales
from product.serializers import ProductListSerializer


class GetSales(APIView):
    def get(self, *args, **kwargs):
        limit = self.request.query_params.get("limit", 16)
        offset = self.request.query_params.get("offset", 0)
        products = get_on_sales(limit=limit, offset=offset)
        serializer = ProductListSerializer(products, many=True)
        return ok(data=serializer.data)
