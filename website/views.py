from django.shortcuts import render, redirect
from .models import Cities
from .forms import CityForm
# Create your views here.

def home(request):
    if Cities.objects.all().count() == 0:
        init_testSet()
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city_input = form.cleaned_data.get("city_input")
            if Cities.objects.filter(name=city_input).exists():
                return redirect('city_lookup', city_name=city_input);
            else:
                print("city does not excists")
        else:
            print("not valid")
    cities = list(Cities.objects.values_list("name", flat=True))
    form=CityForm()
    return render(request, "home.html", {"cities":cities, "form":form})

def cityLookup(request, city_name):
    #redirect complete
    print(city_name)
    return render(request,"bootstrap.html")


def init_testSet():
     Cities(name="Chico").save()
     Cities(name="Sunnyvale").save()
     Cities(name="SanFrancisco").save()
     Cities(name="SanJose").save()
     Cities(name="Mountain View").save()
     Cities(name="Palo Alto").save()
