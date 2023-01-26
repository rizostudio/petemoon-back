from django.urls import path

from .views import PetShopProductsView

urlpatterns = [
    path("products", PetShopProductsView.as_view(), name="products"),
]
