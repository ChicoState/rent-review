from django.contrib import admin
from website.models import Cities

# Register your models here.
# class CitiesAdmin(admin.ModelAdmin):
#     fields = (name, complex_name)

admin.site.register(Cities)
