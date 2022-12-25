from dashboard.views import (
    PetViewSet, AddressViewSet, OrdersViewSet

)


def register_routes(router):
    router.register("dashboard/address", AddressViewSet, basename='address')
    router.register("dashboard/pet", PetViewSet, basename='pet')
    router.register("dashboard/order", OrdersViewSet, basename='order')
