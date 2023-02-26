from django.urls import path
from .views import CartView, OrderView, ShippingView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('order', OrderView.as_view(), name='order'),
    path('order/<int:id>', OrderView.as_view(), name='order'),
    path('shipping', ShippingView.as_view(), name='order'),

]
