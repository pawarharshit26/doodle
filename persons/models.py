from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Follower_table(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE,related_name='person_who_follow')
    following = models.ForeignKey(User, on_delete=models.CASCADE,related_name='person_who_followed')

    def __str__(self):
        return f'{self.follower} follow {self.following}'


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,)
    profile_picture = models.ImageField(upload_to = 'persons/profile_images',default="persons/profile_images/default_pic.png")
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length = 5)

    def __str__(self):
        return self.user.username