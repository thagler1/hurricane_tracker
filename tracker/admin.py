from django.contrib import admin
from django.contrib.gis import admin
from .models import Storm, Advisory, Posts
# Register your models here.

admin.site.register(Storm,  admin.GeoModelAdmin)
admin.site.register(Advisory)
admin.site.register(Posts)