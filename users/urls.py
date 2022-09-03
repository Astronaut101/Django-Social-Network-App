# users/urls.py

from django.conf.urls import include
from django.conf.urls import url

from .views import signin_dashboard


app_name = "users"


urlpatterns = [
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^signin_dashboard/", signin_dashboard, name="signin_dashboard"),
]