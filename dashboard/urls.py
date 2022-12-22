from .views import (
    PetViewSet,
  
)


def register_routes(router):
    router.register("dashboard", PetViewSet, basename='pet')
    
