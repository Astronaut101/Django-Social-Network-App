from django.shortcuts import render

# Create your views here.
from django.shortcuts import render


def signin_dashboard(request):
    return render(request, "users/signin_dashboard.html")
 