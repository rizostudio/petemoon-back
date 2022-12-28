from django.urls import path

from accounts.views import Refresh, Register, SendOTP, VerifyOTP

urlpatterns = [
    path("otp/", SendOTP.as_view(), name="send_otp"),
    path("otp/verify/", VerifyOTP.as_view(), name="verify_otp"),
    path("refresh/", Refresh.as_view(), name="refresh"),
    path("register/", Register.as_view(), name="register"),
]
