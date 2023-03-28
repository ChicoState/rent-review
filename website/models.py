from django.db import models
from django.contrib.auth.models import User
from star_ratings.models import Rating
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Avg
from django.core.validators import MaxValueValidator
# Create your models here.


class Cities(models.Model):
    name = models.CharField(max_length=28)
    complex_name = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    url = models.CharField(max_length=128)
    zipcode = models.IntegerField()

    def average_ratings(self) -> dict:
        averages = {}
        averages["likes_avg"] = Posts.objects.filter(ComplexID=self).aggregate(Avg("likes"))["likes__avg"] or 0
        averages["strictness_avg"] = Posts.objects.filter(ComplexID=self).aggregate(Avg("strictness"))["strictness__avg"] or 0
        averages["amennities_avg"] = Posts.objects.filter(ComplexID=self).aggregate(Avg("amennities"))["amennities__avg"] or 0
        averages["accessibility_avg"] = Posts.objects.filter(ComplexID=self).aggregate(Avg("accessibility"))["accessibility__avg"] or 0
        averages["maintenence_avg"] = Posts.objects.filter(ComplexID=self).aggregate(Avg("maintenence"))["maintenence__avg"] or 0
        averages["grace_period_avg"] = Posts.objects.filter(ComplexID=self).aggregate(Avg("grace_period"))["grace_period__avg"] or 0
        averages["staff_friendlyness_avg"] = Posts.objects.filter(ComplexID=self).aggregate(Avg("staff_friendlyness"))["staff_friendlyness__avg"] or 0
        averages["price_avg"] = Posts.objects.filter(ComplexID=self).aggregate(Avg("price"))["price__avg"] or 0
        return averages

    def __str__(self):
        return f"{self.name}: {self.average_rating()}"


class Posts(models.Model):
    # Look into this?
    # https://pypi.org/project/django-star-ratings/
    # example implementation for input forms https://medium.com/geekculture/django-implementing-star-rating-e1deff03bb1c
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    complex = models.ForeignKey(Cities, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=128)
    post_text = models.CharField(max_length=1028)
    likes = models.IntegerField(default=0,validators=[MaxValueValidator(5)])
    strictness = models.IntegerField(default=0,validators=[MaxValueValidator(5)])
    amennities = models.IntegerField(default=0,validators=[MaxValueValidator(5)])
    accessibility = models.IntegerField(default=0,validators=[MaxValueValidator(5)])
    maintenence = models.IntegerField(default=0,validators=[MaxValueValidator(5)])
    grace_period = models.IntegerField(default=0,validators=[MaxValueValidator(5)])
    staff_friendlyness = models.IntegerField(default=0,validators=[MaxValueValidator(5)])
    price = models.IntegerField(default=0,validators=[MaxValueValidator(5)])
    dateCreated = models.DateField(auto_now_add=True)


class Comments(models.Model):
    PostID = models.ForeignKey(Posts, on_delete=models.CASCADE)
    CommentText = models.CharField(max_length=512)
    dateCreated = models.DateField(auto_now=True)
