# users/urls.py

# from django.conf.urls import url
from django.urls import path

from .views import signin_dashboard

app_name = "users"

urlpatterns = [
    path("signin_dashboard/", signin_dashboard, name="signin_dashboard"),
]