# Create your views here.

from django.contrib.auth import login
# from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from users.forms import CustomUserCreationForm


def signin_dashboard(request):
    return render(request, "users/signin_dashboard.html")
 

def register(request):
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST or None)
        if form.is_valid():
            # Changing our code line below from 'user = form.save()' into `user = form.save(commit=False)`
            # to pass in the original login template that our web app is using. 
            user = form.save(commit=False)
            # This code tells Django that we are acknowledging Social Media / Third Party Authentication
            # and the original Django Authentication.
            user.backend = "django.contrib.auth.backends.ModelBackend"
            user.save()
            login(request, user)
            return redirect(reverse("users:signin_dashboard"))
        else:
            return redirect(reverse("users:register"))
