from django.shortcuts import render, redirect
from .models import Cities, Posts, Comments, User
from django.db.models import Avg
from .forms import imageForm, CityForm, LoginForm, JoinForm, CreateComplexForm, CommentForm
#from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.encoding import iri_to_uri
#
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
        cities = list(Cities.objects.filter(
            name__icontains=city_name).order_by("complex_name"))
    context = {"cities": cities}
    # for i in range(len(cities)):
    #     print(cities[i].name, cities[i].complex_name)
    return render(request, "complexDisplay.html", context=context)




def complexLookup(request, city_name, complex_id):
    if city_name == "" or not complex_id:
        return redirect('home')

    city = list(Cities.objects.filter(pk=complex_id))
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

    city = list(Cities.objects.filter(pk=complex_id))
    
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

# Posts(user=User.objects.filter(username="admin"),complex=Cities.objects.filter(name__icontains="chico"), post_title="testing",post_text="test test test", likes=2, strictness=3,amennities=1,accessibility=0,maintenence=5,grace_period=4,staff_friendlyness=0,price=5).save()


def join(request):
    if (request.method == "POST"):
        join_form = JoinForm(request.POST)
        if (join_form.is_valid()):
            user = join_form.save()
            user.set_password(user.password)
            user.save()
            return redirect("home")
        else:
            return render(request, "join.html", {"join_form": join_form})
    else:
        return render(request, "join.html", {"join_form": JoinForm})


def user_login(request):
    # print("in login function")
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
                    redirect_to = request.GET['next']
                    print(redirect_to)
                    url_is_safe = url_has_allowed_host_and_scheme(redirect_to, None)
                    if url_is_safe:
                        url = iri_to_uri(redirect_to)
                        return redirect(url)
                    return redirect('home')
                else:
                    print("user not active")
                    return HttpResponse("Your account is not active.")
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
            form.save()
            return redirect("home")
    else:
        form = CreateComplexForm()
    context = {'form': form}
    return render(request, "createComplex.html", context=context)


def image_upload_view(request):
    if request.method == 'POST':
        form=imageForm(request,POST,request.FILES)
        if form.is_valid():
            form.save()
            imag_obj = form.instance
            return render(request, 'imageUpload.html',{'form':form,'imag_obj':imag_obj})
    else:
        form = imageForm()
        return render(request, 'imageUpload.html',{'form':form})