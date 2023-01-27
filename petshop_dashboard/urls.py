from django.urls import path

from .views import PetShopProductPricingView, ProductsView

urlpatterns = [
    path("product-pricing", PetShopProductPricingView.as_view(), name="product-pricing"),
    path("product-pricing/<int:id>", PetShopProductPricingView.as_view(), name="product-pricing"),
    path("products", ProductsView.as_view(), name="products"),


]
