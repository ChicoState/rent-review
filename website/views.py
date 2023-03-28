from django.shortcuts import render, redirect
from .models import Cities, Posts, Comments
from .forms import CityForm
# Create your views here.


def home(request):
    if Cities.objects.all().count() == 0:
        init_testSet()
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city_input = form.cleaned_data.get("city_input")
            if Cities.objects.filter(name__icontains=city_input).exists():
                return redirect('city_lookup', city_name=city_input)
            else:
                print("city does not excists")
        else:
            print("not valid")
    cities = list(set(Cities.objects.values_list("name", flat=True)))
    form = CityForm()
    return render(request, "home.html", {"cities": cities, "form": form})


def cityLookup(request, city_name):
    # redirect complete
    # If city name is empty
    if city_name == "":
        return redirect('home')
    else:
        cities = list(Cities.objects.filter(name__icontains=city_name).order_by("complex_name"))
    context = {"cities": cities}
    for i in range(len(cities)):
        print(cities[i].name, cities[i].complex_name)
    return render(request, "complexDisplay.html", context=context)




def complexLookup(request, city_name, complexe_id):
    if city_name == "" or not complexe_id:
        return redirect('home')
    context = 
    city = Cities.objects.filter(id=complexe_id)
    post_list = list(Posts.objects.filter(complexe__pk=complexe_id).only("user", "post_title", "likes"))
    complexe_data = {}
    complexe_data["likes_avg"] = Posts.objects.filter(complexe__pk=complexe_id).aggregate(Avg("likes"))["likes__avg"] or 0
    complexe_data["strictness_avg"] = Posts.objects.filter(complexe__pk=complexe_id).aggregate(Avg("strictness"))["strictness__avg"] or 0
    complexe_data["amennities_avg"] = Posts.objects.filter(complexe__pk=complexe_id).aggregate(Avg("amennities"))["amennities__avg"] or 0
    complexe_data["accessibility_avg"] = Posts.objects.filter(complexe__pk=complexe_id).aggregate(Avg("accessibility"))["accessibility__avg"] or 0
    complexe_data["maintenence_avg"] = Posts.objects.filter(complexe__pk=complexe_id).aggregate(Avg("maintenence"))["maintenence__avg"] or 0
    complexe_data["grace_period_avg"] = Posts.objects.filter(complexe__pk=complexe_id).aggregate(Avg("grace_period"))["grace_period__avg"] or 0
    complexe_data["staff_friendlyness_avg"] = Posts.objects.filter(complexe__pk=complexe_id).aggregate(Avg("staff_friendlyness"))["staff_friendlyness__avg"] or 0
    complexe_data["price_avg"] = Posts.objects.filter(complexe__pk=complexe_id).aggregate(Avg("price"))["price__avg"] or 0

    context = {"city": city, "complexe_data": complexe_data, "display_list" : post_list}
    return  render(request, "postDisplay.html", context)

def postLookup(request, city_name, complexe_id, post_id):
    
    return redirect('home')





def init_testSet():
    print("SAVING INTO DATABASE\n")
    from csv import DictReader
    #! If error on open check to see if path is correct.
    for row in DictReader(open("static/misc/TempDatabaseEntries.csv")):
        DBentry = Cities(
            name=row["City"],
            complex_name=row["complex_name"],
            address=row["address"],
            url=row["url"],
            zipcode=row["zipcode"],
        )
        DBentry.save()
