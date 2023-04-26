"""RentReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.urls.conf import include
#from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static 

from website import views as website_view
from website.views import  *

urlpatterns = [
    path("admin/", admin.site.urls, name="adminPage"),
    path('', website_view.home, name="home"),
    path('display_hotel_images/<complex_id>/', website_view.display_hotel_images,  name='display_hotel_images'),
    path('city_lookup/<city_name>/', website_view.cityLookup,  name='city_lookup'),
    path('complexLookup/<city_name>/<complex_id>/', website_view.complexLookup,  name='complexLookup'),
    path('add_post/<city_name>/<complex_id>/addPost', website_view.add_post,  name='add_post'),
    path('post/<city_name>/<complex_id>/<post_id>', website_view.postLookup,  name='postLookup'),
    path('/join/', website_view.join, name='join'),
    path('/login/', website_view.user_login, name='login'),
    path('/logout/', website_view.user_logout, name='logout'),
    #path('/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    #path('/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path("/createComplex/", website_view.createComplex, name="createComplex"),
    #path('/upload/', website_view.image_upload_view),
    path('image_upload/', website_view.hotel_image_view, name='image_upload'),
    path('success/', website_view.success, name='success'),
    path('hotel_images/', website_view.display_hotel_images, name = 'hotel_images'),

] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)