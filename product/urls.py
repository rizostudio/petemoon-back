from django.urls import path

from product.views import GetItem

urlpatterns = [
    path("<slug:slug>/", GetItem.as_view(), name="get_item"),
]
