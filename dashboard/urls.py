from django.urls import include, path
from dashboard.views import AddressView


urlpatterns = [
    path('address/', AddressView.as_view(),name='address'),
    path('address/<int:id>', AddressView.as_view(),name='address'),
]
