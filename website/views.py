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
                return redirect('city_lookup', city_name=city_input)
            else:
                print("city does not excists")
        else:
            print("not valid")
    cities = list(set(Cities.objects.values_list("name", flat=True)))
    form = CityForm()
    print(cities)
    return render(request, "home.html", {"cities": cities, "form": form})


def cityLookup(request, city_name):
    # redirect complete
    print(city_name)
    # If city name is empty
    if city_name == "":
        return redirect('home')
    else:
        cities = list(Cities.objects.filter(
            name=city_name).order_by("complex_name"))
    context = {"cities": cities}
    for i in range(len(cities)):
        print(cities[i].name, cities[i].complex_name)
    return render(request, "complexDisplay.html", context=context)


def init_testSet():
    print("SAVING INTO DATABASE\n")
    Cities(name="Chico", complex_name="Village At the Timbers").save()
    Cities(name="Chico", complex_name="Timbers IV").save()
    Cities(name="Sunnyvale", complex_name="Arioso Apt").save()
    Cities(name="Sunnyvale", complex_name="Santa Clara Apt").save()
    Cities(name="SanFrancisco", complex_name="Com 1").save()
    Cities(name="SanFrancisco", complex_name="Com 2").save()
    Cities(name="SanFrancisco", complex_name="Com 3").save()
    Cities(name="SanJose", complex_name="SJ Com 3").save()
    Cities(name="Mountain View", complex_name="MV Com 3").save()
    Cities(name="Palo Alto", complex_name="PA Com 3").save()
