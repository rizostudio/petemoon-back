from django.urls import path
from .views import PotentialTimeView

urlpatterns = [
    path('potential-time', PotentialTimeView.as_view(), name='potential-time'),


]
