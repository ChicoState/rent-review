from django.shortcuts import render, redirect
from .models import City, Posts, Comments, User, Complex
from django.db.models import Avg
from .forms import CityForm, LoginForm, NewUserForm, CreateComplexForm, CommentForm, RateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.encoding import iri_to_uri
from django.contrib import messages
import requests
import os
from dotenv import load_dotenv
from pathlib import Path
import json

init = False

if not init:
    dotenv_path = Path(os.path.dirname(__file__) + '/../.env')
    load_dotenv(dotenv_path=dotenv_path)
    init = True


def home(request):
    
    if Complex.objects.all().count() == 0:
        init_testSet()
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city_input = form.cleaned_data.get("city_input")
            if City.objects.filter(name__icontains=city_input).exists():
                return redirect('city_lookup', city_name=city_input.capitalize())
            else:
                print("City does not exist")
        else:
            print("Not Valid")
    cities = list(set(City.objects.values_list("name", flat=True)))
    form = CityForm()
    return render(request, "home.html", {"cities": cities, "form": form})

def cityLookup(request, city_name):
    # redirect complete
    # If city name is empty
    if city_name == "":
        return redirect('home')
    else:
        if City.objects.filter(name=city_name).exists():
            city_lat = list(City.objects.filter(name=city_name).values_list("lat", flat=True))
            city_lng = list(City.objects.filter(name=city_name).values_list("lng", flat=True))
            print(city_lat)
            print(city_name)
            print(city_lng)

            city_center = [city_lat[0],city_lng[0]]
        else:
            city_center = [0,0]
        print(city_center)
        complexs = list(Complex.objects.filter(
            city_name__name__contains=city_name).order_by("complex_name"))
        coordinates = []
        for c in complexs:
            
            coordinates.append(["%s" % c.complex_name,c.lat,c.lng])
        context = {"cities": complexs,"city_center":city_center, "coordinates":coordinates, "googleApiKey": os.environ.get('GOOGLE_MAPS_API_KEY'),}
        # for i in range(len(cities)):
        #     print(cities[i].name, cities[i].complex_name)
        return render(request, "complexDisplay.html", context=context)

def complexLookup(request, city_name, complex_id):
    if city_name == "" or not complex_id:
        return redirect('home')

    city = list(Complex.objects.filter(pk=complex_id))
    print(city)
    post_list = list(Posts.objects.filter(complex__pk=complex_id).only(
        "user", "post_title", "likes", "id"))
    complex_data = {}
    complex_data["Strictness"] = Posts.objects.filter(complex__pk=complex_id).aggregate(Avg("strictness"))["strictness__avg"] or 0
    complex_data["Amennities"] = Posts.objects.filter(complex__pk=complex_id).aggregate(Avg("amennities"))["amennities__avg"] or 0
    complex_data["Accessibility"] = Posts.objects.filter(complex__pk=complex_id).aggregate(Avg("accessibility"))["accessibility__avg"] or 0
    complex_data["Maintenence"] = Posts.objects.filter(complex__pk=complex_id).aggregate(Avg("maintenence"))["maintenence__avg"] or 0
    complex_data["Grace Period"] = Posts.objects.filter(complex__pk=complex_id).aggregate(Avg("grace_period"))["grace_period__avg"] or 0
    complex_data["Staff Friendlyness"] = Posts.objects.filter(complex__pk=complex_id).aggregate(Avg("staff_friendlyness"))["staff_friendlyness__avg"] or 0
    complex_data["Price"] = Posts.objects.filter(complex__pk=complex_id).aggregate(Avg("price"))["price__avg"] or 0
    complex_likes = Posts.objects.filter(complex__pk=complex_id).aggregate(Avg("likes"))["likes__avg"] or 0
    for key,value in complex_data.items():
        print(key)
        print(value)
    print(post_list)
    context = {"city": city[0],"complex_likes":complex_likes, "complex_data": complex_data, "post_list" : post_list}
    return  render(request, "postDisplay.html", context)

def postLookup(request, city_name, complex_id, post_id):
    if city_name == "" or not complex_id or not post_id:
        return redirect('home')
    post_obj = Posts.objects.filter(pk=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_input = form.cleaned_data.get("comment_text")
            new_comment = Comments(post_id = post_id, user_id = request.user.id, comment_text = comment_input)
            new_comment.save()
            return redirect('postLookup', city_name=city_name, complex_id=complex_id, post_id=post_id)           
        else:
            print("not valid comment")

    city = list(Complex.objects.filter(pk=complex_id))
    
    post_data = list(post_obj.values("strictness","amennities","accessibility","maintenence","grace_period","staff_friendlyness"))
    post_data = dict( sorted(post_data[0].items(), key=lambda x: x[0].lower()) )
    comment_list = list(Comments.objects.filter(post__pk = post_id).only("user","comment_text", "date_created"))
    complex_likes = list(Posts.objects.filter(pk=post_id).values("likes"))[0]
    user = list(Posts.objects.filter(pk=post_id).only("user"))[0]
    post_description = list(Posts.objects.filter(pk=post_id).only(
        "post_title", "post_text", "date_created"))[0]

    context = {"city": city[0],"complex_likes":complex_likes, "post_data": post_data, "comment_list" : comment_list, "user": user, "post_description": post_description, "form" : CommentForm}
    return  render(request, "commentDisplay.html", context)

def add_post(request, city_name, complex_id):
    if (request.method == "POST"):
        form = RateForm(request.POST)
        if form.is_valid():
            new_post = Posts(user_id = request.user.id,
                             complex_id = complex_id,
                             post_title = form.cleaned_data.get("post_title"),
                             post_text = form.cleaned_data.get("post_text"),
                             likes = form.cleaned_data.get("likes"),
                             strictness = form.cleaned_data.get("strictness"),
                             amennities = form.cleaned_data.get("amennities"),
                             accessibility = form.cleaned_data.get("accessibility"),
                             maintenence = form.cleaned_data.get("maintenence"),
                             grace_period = form.cleaned_data.get("grace_period"),
                             staff_friendlyness = form.cleaned_data.get("staff_friendlyness"),
                             price = form.cleaned_data.get("price"))
            new_post.save()
            redirect_to = request.GET['next']
            print(redirect_to)
            url_is_safe = url_has_allowed_host_and_scheme(redirect_to, None)
            if url_is_safe:
                url = iri_to_uri(redirect_to)
                return redirect(url)
            else:
                return redirect("home")
    else:
        form = RateForm()
    context = {
        'form': form
        }
    return render(request, 'reviewDisplay.html', context=context)

def init_testSet():
    print("SAVING INTO DATABASE\n")
    from csv import DictReader
    #! If error on open check to see if path is correct.
    for row in DictReader(open("static/misc/us-cities-top-1k.csv")):
        DBentry = City(
            name=row["City"],
            lat=row["lat"],
            lng=row["lon"],
            state=row["State"],
            
        )
        DBentry.save()
    
    for row in DictReader(open("static/misc/TempDatabaseEntries.csv")):
        city_id = City.objects.filter(name = row["City"]).values_list('id', flat=True)
        if City.objects.filter(name = row["City"]).exists():
            print(city_id)
            DBentry = Complex(
                city_name_id=city_id,
                complex_name=row["complex_name"],
                address=row["address"],
                url=row["url"],
                zipcode=row["zipcode"],
            )
            DBentry.save()
    

def join(request):
    print("in join request")
    if (request.method == "POST"):
        form = NewUserForm(request.POST)
        if form.is_valid():
            print("join form is valid")
            user = form.save()
            print(user)
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="join.html", context={"join_form":form})


def user_login(request):
    print("in login function")
    if (request.method == 'POST'):
        form = LoginForm(request.POST)
        if form.is_valid():
            print("form is valid")
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    print("user loggedin")
                    redirect_to = request.POST['next']
                    print(redirect_to)
                    url_is_safe = url_has_allowed_host_and_scheme(redirect_to, None)
                    if url_is_safe:
                        url = iri_to_uri(redirect_to)
                        return redirect(url)
                    return redirect('home')
                else:
                    print("user not active")
                    return redirect('home')
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
                return render(request,  "login.html", {"form": LoginForm})
    else:
        print("initial render")
        return render(request, "login.html", {"form": LoginForm})


@login_required(login_url='login/')
def user_logout(request):
    logout(request)
    redirect_to = request.GET['next']
    print(redirect_to)
    url_is_safe = url_has_allowed_host_and_scheme(redirect_to, None)
    if url_is_safe:
        url = iri_to_uri(redirect_to)
        return redirect(url)
    return redirect('home')


def createComplex(request):
    if request.method == "POST":
        form = CreateComplexForm(request.POST)
        if form.is_valid():
            new_complex = form.save()
            full_address = str(new_complex.address) +", "+ str(new_complex.zipcode)
            lat,lng = extract_lat_long_via_address(full_address)
            new_complex.lat = lat
            new_complex.lng = lng
            new_complex.save(update_fields=['lat','lng'])
            return redirect("complexLookup", city_name=new_complex.city_name.name, complex_id=new_complex.pk)
    else:
        form = CreateComplexForm()
    context = {'form': form}
    return render(request, "createComplex.html", context=context)


 

def extract_lat_long_via_address(address_or_zipcode):
    lat, lng = None, None
    api_key = os.environ.get('GOOGLE_GEOCODING_API_KEY')
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    endpoint = f"{base_url}?address={address_or_zipcode}&key={api_key}"
    # see how our endpoint includes our API key? Yes this is yet another reason to restrict the key
    r = requests.get(endpoint)
    if r.status_code not in range(200, 299):
        return None, None
    try:
        '''
        This try block incase any of our inputs are invalid. This is done instead
        of actually writing out handlers for all kinds of responses.
        '''
        results = r.json()['results'][0]
        lat = results['geometry']['location']['lat']
        lng = results['geometry']['location']['lng']
    except:
        pass
    return lat, lng
