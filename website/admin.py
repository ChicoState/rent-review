from django.contrib import admin
from .models import Cities

# Register your models here.
class CitiesAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Cities,CitiesAdmin)
