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


