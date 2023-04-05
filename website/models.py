from django.db import models

# Create your models here.


class Cities(models.Model):
    name = models.CharField(max_length=28)
    complex_name = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    url = models.CharField(max_length=128)
    zipcode = models.IntegerField()
    citis_images = models.ImageField(upload_to='images/')
##
# the upload_to takes care of the directory the image is being uploaded to
# #
    def __str__(self):
        return f"{self.name}"


