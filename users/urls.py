# users/urls.py

from django.urls import path
from django.conf.urls import include
from django.conf.urls import url

from .views import signin_dashboard
from .views import register

app_name = "users"


urlpatterns = [
    path("", signin_dashboard, name="signin_dashboard"),
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^register/", register, name="register"),
]