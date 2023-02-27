from django.db import models

# Create your models here.
class Cities(models.Model):
    name = models.CharField(max_length=28)

    def __str__(self):
        return f"{self.name}"
