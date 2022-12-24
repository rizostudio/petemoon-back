from .views import (
    PetViewSet, AddressViewSet, ProfileViewSet
  
)


def register_routes(router):
    router.register("dashboard/address", AddressViewSet, basename='address')
    router.register("dashboard/pet", PetViewSet, basename='pet')
    router.register("dashboard/profile", ProfileViewSet, basename='profile')
    
