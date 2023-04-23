from django.contrib import admin
from website.models import City, Posts, Comments, Complex

# Register your models here.
# class CitiesAdmin(admin.ModelAdmin):
#     fields = (name, complex_name)

admin.site.register(City)
admin.site.register(Complex)
admin.site.register(Posts)
admin.site.register(Comments)