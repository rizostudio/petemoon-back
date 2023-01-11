from django.urls import path
from .views import CartView

urlpatterns = [
    path('add-product/', CartView.as_view(), name='cart'),

]
