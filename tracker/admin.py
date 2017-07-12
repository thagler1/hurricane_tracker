from django.contrib import admin
from .models import Storm, Advisory
# Register your models here.

admin.site.register(Storm)
admin.site.register(Advisory)