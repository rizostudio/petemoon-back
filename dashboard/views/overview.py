from django.utils.translation import gettext_lazy as _

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from config.responses import SuccessResponse
from dashboard.serializers import PetGetSerializer
from dashboard.models import Pet
from shopping_cart.models import Order
from django.db.models import Sum, Q


class OverViewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        pet = Pet.objects.filter(user=request.user)
        wallet = request.user.wallet.credit
        orders = Order.objects.filter(user=request.user)

        orders_count = orders.count()

        delivered = Order.objects.filter(user=request.user,status="DELIVERED").count()
        canceled = Order.objects.filter(user=request.user,status="CANCELED").count()
        ongoing = Order.objects.filter(user=request.user,status="ONGOING").count()
        total_price = Order.objects.filter(Q(user=request.user) 
            & ( Q(status="ONGOING") |
                Q(status="SENDING") |
                Q(status="PROCESSING") ) ).aggregate(Sum('total_price'))

        pet = PetGetSerializer(pet, many=True).data
        print(total_price)
        return SuccessResponse(
            data={"my_pet": pet,
                    "wallet": wallet, 
                    "orders":{"delivered": delivered, "canceled": canceled, "ongoing": ongoing},
                    "total_price": total_price['total_price__sum'],
                    "orders_count":orders_count
            })
