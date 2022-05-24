from django.contrib import admin

# Register your models here.
from .models import Package, Investment

admin.site.register(Package)
admin.site.register(Investment)
