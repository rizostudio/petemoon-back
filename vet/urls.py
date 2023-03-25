from django.urls import path
from .views import (
    PotentialTimeView, AvailableReserveTimeView, VetSingleView,
      VisitView, PastVisitView,SinglePastVisitView, FutureVisitView,SingleFutureVisitView)

urlpatterns = [
    path('potential-time', PotentialTimeView.as_view(), name='potential-time'),
    path('available-time', AvailableReserveTimeView.as_view(), name='available-time'),
    path('vet-single', VetSingleView.as_view(), name='vet-single'),
    path('visit', VisitView.as_view(), name='visit'),
    path('past-visit', PastVisitView.as_view(), name='past-visit'),
    path('single-past-visit/<int:id>', SinglePastVisitView.as_view(), name='past-visit'),
    path('future-visit', FutureVisitView.as_view(), name='future-visit'),
    path('single-future-visit/<int:id>', SingleFutureVisitView.as_view(), name='single-future-visit'),
]
