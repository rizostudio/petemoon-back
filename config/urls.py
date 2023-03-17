"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config.settings import STATIC_ROOT, STATIC_URL, SWAGGER_URL
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
if SWAGGER_URL is not None:
    urlpatterns += [path(SWAGGER_URL, yaml_to_html)]

urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
