from rest_framework.views import APIView

from config.responses import ok
from product.selectors import get_top_seller
from product.serializers import PetshopGetSerializer


class GetTopSellers(APIView):
    def get(self, request):
        top_sellers = get_top_seller()
        serializer = PetshopGetSerializer(top_sellers, many=True)
        return ok(serializer.data)
