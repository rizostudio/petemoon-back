from django.urls import path

from accounts.views import (
    Logout,
    Refresh,
    Register,
    RegisterPetshop,
    SendOTP,
    VerifyOTP,
)

urlpatterns = [
    path("otp/", SendOTP.as_view(), name="send_otp"),
    path("otp/verify/", VerifyOTP.as_view(), name="verify_otp"),
    path("refresh/", Refresh.as_view(), name="refresh"),
    path("register/", Register.as_view(), name="register"),
    path(
        "register/petshop/", RegisterPetshop.as_view(), name="register_petshop"
    ),
    path("logout/", Logout.as_view(), name="logout"),
]
