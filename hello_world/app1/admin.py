from django.contrib import admin
# Import models and the class we want to access in Django Admin
from .models import Friends

# Register your models here.
admin.site.register(Friends)