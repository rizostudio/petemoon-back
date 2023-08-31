from django.urls import path

from .views import (
    PotentialTimeView, AvailableReserveTimeView, VetSingleView, VetProfileView, AvailableReserveForNormalUserView, AvailableTimesView,
    ReserveForNormalUserView, VisitView, PastVisitView,SinglePastVisitView, FutureVisitView, VetDashboardView, SingleVisitView,
    SingleFutureVisitView, VetListView, UserFutureVisitView, UserSingleFutureVisitView, UserPastVisitView, UserSinglePastVisitView)


urlpatterns = [
    path('potential-time', PotentialTimeView.as_view(), name='potential-time'),
    path('available-time', AvailableReserveTimeView.as_view(), name='available-time'),
    path('available-times/', AvailableTimesView.as_view(), name='available-times'),
    #path('vet-single', VetSingleView.as_view(), name='vet-single'),
    path('visit', VisitView.as_view(), name='visit'),
    path('single-visit/<int:id>', SingleVisitView.as_view(), name='single-visit'),
    path('past-visit', PastVisitView.as_view(), name='past-visit'),
    path('single-past-visit/<int:id>', SinglePastVisitView.as_view(), name='past-visit'),
    path('future-visit', FutureVisitView.as_view(), name='future-visit'),
    path('single-future-visit/<int:id>', SingleFutureVisitView.as_view(), name='single-future-visit'),
    path('user-future-visit', UserFutureVisitView.as_view(), name='user-future-visit'),
    path('user-single-future-visit/<int:id>', UserSingleFutureVisitView.as_view(), name='user-single-future-visit'),
    path('user-past-visit', UserPastVisitView.as_view(), name='user-past-visit'),
    path('user-single-past-visit/<int:id>', UserSinglePastVisitView.as_view(), name='user-single-past-visit'),
    path('vet-list', VetListView.as_view(), name='vet-list'),
    path('vet-single/<int:id>', VetSingleView.as_view(), name='vet-single'),
    path('vet-profile', VetProfileView.as_view(), name='vet-profile'),
    path('available-reserve/<int:id>', AvailableReserveForNormalUserView.as_view(), name='available-reserve'),
    path('reserve/<int:id>', ReserveForNormalUserView.as_view(), name='reserve'),
    path("dashboard", VetDashboardView.as_view(), name="dashboard"),

]

