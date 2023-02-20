from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework.views import APIView

from accounts.views.permissions import IsPetShopApproved
from config.responses import bad_request, not_found, ok
from product.selectors import add_update_pricing, get_product_id_by_slug
from product.serializers.pricing import AddPricingSerializer


class AddUpdatePricing(APIView):
    permission_classes = [IsPetShopApproved]

    @transaction.atomic
    def patch(self, *args, **kwargs):
        product_slug = kwargs.get("slug")
        product_id = get_product_id_by_slug(product_slug)
        if product_id is None:
            return not_found({"message": _("Product not found.")})
        serializer = AddPricingSerializer(data=self.request.data)
        if not serializer.is_valid():
            return bad_request(serializer.errors)
        data = {
            "petshop_id": self.request.user.petshop_profile.shops.id,
            "product_id": product_id,
        }
        data.update(serializer.data)
        try:
            add_update_pricing(**data)
        except Exception as e:
            print(e)
        return ok({"message": _("Pricing added.")})
