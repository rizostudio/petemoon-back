from django.urls import path
from .views import PotentialTimeView, AvailableReserveTimeView

urlpatterns = [
    path('potential-time', PotentialTimeView.as_view(), name='potential-time'),
    path('available-time', AvailableReserveTimeView.as_view(), name='available-time'),


]
