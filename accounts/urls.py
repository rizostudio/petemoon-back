from django.urls import path

from accounts.views import SendOTP

urlpatterns = [
    path("otp/", SendOTP.as_view(), name="send_otp"),
]
