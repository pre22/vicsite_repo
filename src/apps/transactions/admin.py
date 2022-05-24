from django.contrib import admin
# Register your models here.
from .models import Deposit, Withdraw

admin.site.register(Deposit)
admin.site.register(Withdraw)