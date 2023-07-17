from django.urls import path

from accounts.views import (
    Logout,
    Refresh,
    Register,
    RegisterPetshop,
    SendOTP,
    VerifyOTP,
    VetRegisterView,
    UserValidationView,
)



urlpatterns = [
    path("otp/", SendOTP.as_view(), name="send_otp"),
    path("otp/verify/", VerifyOTP.as_view(), name="verify_otp"),
    path("refresh/", Refresh.as_view(), name="refresh"),
    path("register/", Register.as_view(), name="register"),
    path("register/petshop/", RegisterPetshop.as_view(), name="register_petshop"),
    path("register/vet", VetRegisterView.as_view(), name="vet_register"),
    path("logout/", Logout.as_view(), name="logout"),
    path("user-is-valid", UserValidationView.as_view(), name="is-valid"),

]
