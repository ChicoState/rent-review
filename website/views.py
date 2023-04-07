from django.shortcuts import render, redirect
from .models import Cities
from .forms import CityForm
#################################################################
#Added forms/imports 
#By AGGM
#################################################################
from website.forms import JoinForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from website.forms import JoinForm,LoginForm
######################--END OF ADD--##############################
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
    return render(request, "home.html", {"cities": cities, "form": form})


def cityLookup(request, city_name):
    # redirect complete
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



###############################
#Inserting forms for user to join
#Using HeringsJoing form 
###############################
def join(request):
    if(request.method == "POST"):
        join_form = JoinForm(request.POST)
        if(join_form.is_valid()):
            #SAVE FROM DATA TO DB
            user = join_form.save()
            #ENCRPTS THE PASSWORD
            user.set_passowrd(user.password)
            #SAVES ENCRPTED PASSWORD PASSWORD TO DB
            user.save()
            #Succesfuly saves and redirects to home page
            return redirect('home')
        else:
            #Form was filled incorrectly throwing an error
            page_data = {"join_form":join_form}
            return render(request,'templates/join.html',page_data)
    else:
        join_form=JoinForm()
        page_data={"join_form":join_form}
        return render(request, 'templates/join.html',page_data)
#####################
#Addinf the user login here, fallowing Herryings web notes
#####################
def user_login(request):
    if(request.method == 'POST'):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            #We first get usrName and pssWord
            username =login_form.cleaned_data["username"]
            passowrd = login_form.cleaned_data["password"]
            #Djangos build-in Authentication Functions are being used 
            user=authenticate(username=username,passowrd=passowrd)
            #Checking if we have a user
            if user:
                #Checking the account activity
                if user.is_active:
                    #We log user in and redirect them
                    login(request,user)
                    #Send the User back to the home page
                    return redirect('homes')
                else:
                    #There is no account with said input
                    return HttpResponse("There is no existing account.")
            else:
                print("Someone tried to login and failed.")
                print("The username used: {} and password: {}".format(username,passowrd))
                return render(request, 'templates/login.html',{"login_form":LoginForm})
        else:
            #Nothing was give for user login
            return render(request,'templates/login.html',{"login_form":LoginForm})
##########################################
# #END OF USER LOGIN FORM# #
##########################################
def user_logout(request):
    def user_logout(request):
        #LOGOUT the user
        logout(request)
        return redirect("")
def cities_images_view(request):
    if request.method == 'POST':
        form = CityForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = CityForm()
    return render(request, 'imageUpload.html',{'form':form})

def success(request):
    return HttpResponse('successfully uploaded')