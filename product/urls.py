from django.urls import path

from product.views import GetItem, GetList

urlpatterns = [
    path("", GetList.as_view(), name="item_list"),
    path("<slug:slug>/", GetItem.as_view(), name="get_item"),
]
