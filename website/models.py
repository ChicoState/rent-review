from django.db import models
from django.contrib.auth.models import User
from star_ratings.models import Rating
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MaxValueValidator
# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=28)
    state = models.CharField(max_length=12)
    lat = models.FloatField(default=39.72974839382744)
    lng = models.FloatField(default=-121.84780857997693)
 

class Complex(models.Model):
    city_name = models.ForeignKey(City, on_delete=models.CASCADE)
    complex_name = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    url = models.CharField(max_length=128)
    zipcode = models.IntegerField()
    lat = models.FloatField(default=39.72974839382744)
    lng = models.FloatField(default=-121.84780857997693)

    def __str__(self):
        return f"{self.city_name.name}"

class Posts(models.Model):
    # Look into this?
    # https://pypi.org/project/django-star-ratings/
    # example implementation for input forms https://medium.com/geekculture/django-implementing-star-rating-e1deff03bb1c
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    complex = models.ForeignKey(Complex, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=128)
    post_text = models.CharField(max_length=1028)
    likes = models.IntegerField(default=0, validators=[MaxValueValidator(5)])
    strictness = models.IntegerField(
        default=0, validators=[MaxValueValidator(5)])
    amennities = models.IntegerField(
        default=0, validators=[MaxValueValidator(5)])
    accessibility = models.IntegerField(
        default=0, validators=[MaxValueValidator(5)])
    maintenence = models.IntegerField(
        default=0, validators=[MaxValueValidator(5)])
    grace_period = models.IntegerField(
        default=0, validators=[MaxValueValidator(5)])
    staff_friendlyness = models.IntegerField(
        default=0, validators=[MaxValueValidator(5)])
    price = models.IntegerField(default=0, validators=[MaxValueValidator(5)])
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}, {self.complex}, {self.post_title}"

class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=512)
    date_created = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.post}"
