from .views import (
    PetViewSet,
  
)


def register_routes(router):
    router.register("pet", PetViewSet, basename='pet')
    
