from django.urls import include, path
from dashboard.views import AddressView, PetGeneralView


urlpatterns = [
    path('address/', AddressView.as_view(),name='address'),
    path('address/<int:id>', AddressView.as_view(),name='address'),
    path('pet/', PetGeneralView.as_view(),name='pet'),
    path('pet/<int:id>', PetGeneralView.as_view(),name='pet'),

]
