from .views import (
    PetViewSet, AddressViewSet, ProfileViewSet, OrdersViewSet
  
)


def register_routes(router):
    router.register("dashboard/address", AddressViewSet, basename='address')
    router.register("dashboard/pet", PetViewSet, basename='pet')
    router.register("dashboard/profile", ProfileViewSet, basename='profile')
    router.register("dashboard/order", OrdersViewSet, basename='order')
    
