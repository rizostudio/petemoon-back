from django.urls import path
from .views import PotentialTimeView, AvailableReserveTimeView, VetSingleView, VisitView

urlpatterns = [
    path('potential-time', PotentialTimeView.as_view(), name='potential-time'),
    path('available-time', AvailableReserveTimeView.as_view(), name='available-time'),
    path('vet-single', VetSingleView.as_view(), name='vet-single'),
    path('visit', VisitView.as_view(), name='visit'),


]
