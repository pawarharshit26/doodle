from django.contrib import admin
from .models import Follower_table,Profile
# Register your models here.

admin.site.register((Follower_table,Profile))