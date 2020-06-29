from django.db import models

from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.


class Photo(models.Model):
    sno = models.AutoField(primary_key = True)
    photo = models.ImageField(upload_to = 'images/photos',default="")
    upload_by = models.ForeignKey(User,on_delete = models.CASCADE)
    upload_time = models.DateTimeField(default = now)

    def __str__(self):
        return self.upload_by.username + "  " + str(self.upload_time)

class Likes(models.Model):
    sno  = models.AutoField(primary_key = True)
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    like_at = models.DateTimeField(default = now)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE,default="")

    def __str__(self):
        return "like by" + self.user.username
    

class Comment(models.Model):
    sno = models.AutoField(primary_key = True)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(default = now)
    # parent = models.ForeignKey('self', on_delete=models.CASCADE,default = None,null = True)

    def __str__(self):
        return self.user.username
    