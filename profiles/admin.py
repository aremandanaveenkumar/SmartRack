from django.contrib import admin
from .models import UserProfile, AddressField

# Register your models here.
admin.site.register(UserProfile) 
admin.site.register(AddressField) 