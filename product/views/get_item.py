from django.utils.translation import gettext as _
from rest_framework.views import APIView

from config.responses import not_found, ok
from product.selectors import get_item_by_slug
from product.serializers import ProductGetSerializer


class GetItem(APIView):
    def get(self, *args, **kwargs):
        slug = kwargs.get("slug")
        item = get_item_by_slug(slug)
        if item:
            return ok(ProductGetSerializer(item).data)
        return not_found(errors=[_("Product not found.")])
