from django.utils.translation import gettext as _
from rest_framework.views import APIView

from config.responses import not_found, ok
from product.selectors import get_item_by_slug, get_related_products
from product.serializers import ProductGetSerializer, ProductListSerializer


class GetItem(APIView):
    def get(self, *args, **kwargs):
        slug = kwargs.get("slug")
        item = get_item_by_slug(slug)
        if item:
            related_products = ProductGetSerializer(
                get_related_products(item), many=True
            ).data
            data = dict(ProductGetSerializer(item).data)
            data["related_products"] = related_products
            return ok(data=data)
        return not_found(errors=[_("Product not found.")])
