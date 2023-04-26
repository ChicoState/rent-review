from django.contrib import admin
from website.models import *#Cities, Posts, Comments

# Register your models here.
# class CitiesAdmin(admin.ModelAdmin):
#     fields = (name, complex_name)

admin.site.register(Cities)
admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(Hotel)