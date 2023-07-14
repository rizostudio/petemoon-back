from django.urls import path

from product.views import (
    AddUpdatePricing,
    GetFilters,
    GetList,
    GetRecommended,
    GetSales,
    GetTopSellers,
    SingleItem,
    ProductSearchView,
    CreateComment
)

urlpatterns = [
    path("", GetList.as_view(), name="item_list"),
    path("filters/", GetFilters.as_view(), name="get_filters"),
    path("top-sellers/", GetTopSellers.as_view(), name="get_top_sellers"),
    path("sales/", GetSales.as_view(), name="get_sales"),
    path("recommended/", GetRecommended.as_view(), name="get_recommended"),
    path("<str:slug>/", SingleItem.as_view(), name="item_detail"),
    path("<slug:slug>/pricing/",AddUpdatePricing.as_view(),name="add_update_pricing"),
    path("search",ProductSearchView.as_view(),name="add_update_pricing"),
    path("create_comment/",CreateComment.as_view(),name="create_comment"),

    
]
