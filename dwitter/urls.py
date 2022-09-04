# dwitter/urls.py

from django.urls import path

from .views import dashboard
from .views import profile_list
from .views import profile

app_name = "dwitter"

urlpatterns = [
    path("home/", dashboard, name="dashboard"),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>", profile, name="profile"),
]
