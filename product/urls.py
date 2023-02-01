from django.urls import path

from product.views import AddUpdatePricing, GetList, SingleItem

urlpatterns = [
    path("", GetList.as_view(), name="item_list"),
    path("<slug:slug>/", SingleItem.as_view(), name="item_detail"),
    path(
        "<slug:slug>/pricing/",
        AddUpdatePricing.as_view(),
        name="add_update_pricing",
    ),
]
