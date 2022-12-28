from dashboard.views import (
    PetViewSet, AddressViewSet, OrdersViewSet, FavoriteViewSet

)


def register_routes(router):
    router.register("dashboard/address", AddressViewSet, basename='address')
    router.register("dashboard/pet", PetViewSet, basename='pet')
    router.register("dashboard/order", OrdersViewSet, basename='order')
    router.register("dashboard/favorite", FavoriteViewSet, basename='favorite')
