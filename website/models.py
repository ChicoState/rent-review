from django.db import models

# Create your models here.


class Cities(models.Model):
    name = models.CharField(max_length=28)
    complex_name = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    url = models.CharField(max_length=128)
    zipcode = models.IntegerField()

    def __str__(self):
        return f"{self.name}"


class Posts(models.Model):
    # Look into this?
    # https://pypi.org/project/django-star-ratings/
    stars = (
        (1, "One Star")
        (2, "Two Star")
        (3, "Three Star")
        (4, "Four Star")
        (5, "Five Star")
    )
    ComplexID = models.ForeignKey(Cities, on_delete=models.CASCADE)
    PostTitle = models.CharField(max_length=128)
    PostText = models.CharField(max_length=1028)
    likes = models.IntegerField(max_length=10, default=0)
    strictness = models.IntegerField(choices=stars)
    Amennities = models.IntegerField(choices=stars)
    Accessibility = models.IntegerField(choices=stars)
    Maintenence = models.IntegerField(choices=stars)
    GracePeriod = models.IntegerField(choices=stars)
    StaffFriendlyness = models.IntegerField(choices=stars)
    Price = models.IntegerField(choices=stars)


class Comments(models.Model):
    PostID = models.ForeignKey(Posts, on_delete=models.CASCADE)
    CommentText = models.CharField(max_length=512)
