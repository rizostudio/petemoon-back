from django.urls import path

from product.views import (
    AddUpdatePricing,
    GetFilters,
    GetList,
    GetSales,
    GetTopSellers,
    SingleItem,
)

urlpatterns = [
    path("", GetList.as_view(), name="item_list"),
    path("filters/", GetFilters.as_view(), name="get_filters"),
    path("top-sellers/", GetTopSellers.as_view(), name="get_top_sellers"),
    path("sales/", GetSales.as_view(), name="get_sales"),
    path("<slug:slug>/", SingleItem.as_view(), name="item_detail"),
    path(
        "<slug:slug>/pricing/",
        AddUpdatePricing.as_view(),
        name="add_update_pricing",
    ),
]
