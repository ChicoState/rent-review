from django.shortcuts import render
from .models import Cities
# Create your views here.

def home(request):
    cities = ["cali", "chico"]
    return render(request, "home.html", {"cities":cities})
