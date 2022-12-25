from django.urls import path

from accounts.views import SendOTP, VerifyOTP

urlpatterns = [
    path("otp/", SendOTP.as_view(), name="send_otp"),
    path("otp/verify/", VerifyOTP.as_view(), name="verify_otp"),
]
