from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config.settings import STATIC_ROOT, STATIC_URL, SWAGGER_URL, MEDIA_URL, MEDIA_ROOT
from utils.swagger_view import yaml_to_html


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),  # TODO remove
    path("accounts/", include("accounts.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("product/", include("product.urls")),
    path("cart/", include("shopping_cart.urls")),
    path("petshop-dashboard/", include("petshop_dashboard.urls")),
    path("payment/", include("payment.urls")),
    path("vet/", include("vet.urls")),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)

if SWAGGER_URL is not None:
    urlpatterns += [path(SWAGGER_URL, yaml_to_html)]
