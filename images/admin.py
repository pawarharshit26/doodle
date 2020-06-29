from django.contrib import admin

from .models import Photo,Comment,Likes
# Register your models here.
 
admin.site.register((Photo,Comment,Likes))