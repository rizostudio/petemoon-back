from django.urls import path
from dashboard.views import (
    AddressView, PetView, OrdersView, 
    BookmarkView, MessageView, UserProfileView, 
    OverViewView, PetTypeView, PetCategoryView,WalletView,SinglePetView)


urlpatterns = [
    path('address/', AddressView.as_view(), name='address'),
    path('address/<int:id>', AddressView.as_view(), name='address'),
    path('pet/', PetView.as_view(), name='pet'),
    path('pet/<int:id>', PetView.as_view(), name='pet'),
    path('pet-type', PetTypeView.as_view(), name='pet-type'),
    path('pet-category/<int:id>', PetCategoryView.as_view(), name='pet-category'),
    path('orders', OrdersView.as_view(), name='orders'),
    path('bookmark', BookmarkView.as_view(), name='bookmark'),
    path('bookmark/<int:id>', BookmarkView.as_view(), name='bookmark'),
    path('message', MessageView.as_view(), name='message'),
    path('user-profile', UserProfileView.as_view(), name='user_profile'),
    path('over-view', OverViewView.as_view(), name='over-view'),
    path('wallet', WalletView.as_view(), name='wallet'),
    path('single-pet/<int:id>', SinglePetView.as_view(), name='single-pet'),




]
