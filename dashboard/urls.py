from django.urls import path
from dashboard.views import AddressView, PetView, OrdersView, FavoriteView


urlpatterns = [
    path('address/', AddressView.as_view(),name='address'),
    path('address/<int:id>', AddressView.as_view(),name='address'),
    path('pet/', PetView.as_view(),name='pet'),
    path('pet/<int:id>', PetView.as_view(),name='pet'),
    path('orders', OrdersView.as_view(),name='orders'),
    path('favorite', FavoriteView.as_view(),name='favorite'),
    path('favorite/<int:id>', FavoriteView.as_view(),name='favorite'),

]
