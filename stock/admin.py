from django.contrib import admin

# Register your models here.

from .models import Stock, Location


admin.site.register(Stock)
admin.site.register(Location)