from django.urls import path

from product.views import GetList, SingleItem

urlpatterns = [
    path("", GetList.as_view(), name="item_list"),
    path("<slug:slug>/", SingleItem.as_view(), name="item_detail"),
]
