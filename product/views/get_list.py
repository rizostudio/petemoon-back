from rest_framework.views import APIView

from config.responses import ok
from product.selectors import get_item_list
from product.serializers import ProductListSerializer


class GetList(APIView):
    def get(self, *args, **kwargs):
        query_params = self.request.query_params
        try:
            kw = {
                "limit": int(query_params.get("limit", "16")),
                "offset": int(query_params.get("limit", "0")),
                "pet_types": query_params.get("pet_types", "").split(","),
                "category_slugs": query_params.get("category_slugs", "").split(
                    ","
                ),
                "brand_slugs": query_params.get("brand_slugs", "").split(","),
                "max_price": int(query_params.get("max_price", None)),
                "min_price": int(query_params.get("min_price", None)),
                "order_by": query_params.get("order_by"),
            }
        except Exception:
            kw = {}
        items, count = get_item_list(**kw)
        return ok(
            {
                "products": ProductListSerializer(items, many=True).data,
                "count": count,
            }
        )
