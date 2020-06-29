from django.shortcuts import render,redirect
from django.http import HttpResponse

from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth import login ,logout

from django.contrib.auth.models import User
from .models import Profile
from images.models import Photo
from .models import Follower_table
from images.forms import ImageuploadForm

# Create your views here.
def persons_pro(request):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user = user)
        photos = Photo.objects.none()
        i_follow = Follower_table.objects.none()
        my_followers = Follower_table.objects.none()
        if Photo.objects.filter(upload_by = user).exists():
            photos = Photo.objects.filter(upload_by = user)
        if Follower_table.objects.filter(following = user).exists():
            my_followers = Follower_table.objects.filter(following = user)
        if Follower_table.objects.filter(follower = user).exists():
            i_follow = Follower_table.objects.filter(follower = user)
        d = {'user':user,'profile':profile,'photos':photos,'i_follow':i_follow,'my_followers':my_followers}
        # print(user.username)
        return render(request,'persons/profile.html',d)
    else:
        return HttpResponse('error 404')


def edit_profile_page(request):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user = user)
        d = {'first_name':None,'last_name':None,'dob':None}
        d['username'] = user.username
        if user.first_name != "":
            d['first_name'] = user.first_name
        if user.last_name != "":
            d['last_name'] = user.last_name
        if profile.date_of_birth != None:
            d['dob'] = profile.date_of_birth
            print(d['dob'])
        return render(request,'persons/edit_profile_page.html',d)
    else:
        return HttpResponse('error occure')

def edit_profile(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dob = request.POST['dob']
        
        if request.user.is_authenticated:
            user = request.user
            profile = Profile.objects.get(user = user)
            if username != user.username:
                user.username = username
            if first_name != user.first_name:
                user.first_name  = first_name
            if last_name != user.last_name:
                user.last_name = last_name
            if  dob != profile.date_of_birth:
                profile.date_of_birth != dob

            user.save()
            profile.save()
            return redirect('edit_profile_page')

        else:
            return HttpResponse("user not authenticated")

    return HttpResponse('error get')

def change_password(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user
            old_pass = request.POST['old_pass']
            if check_password(old_pass,user.password):
                new_pass = request.POST['new_pass']
                con_new_pass = request.POST['con_new_pass']
                if new_pass != con_new_pass:
                    messages.error(request, 'please provide same password in both fields')
                    return redirect('edit_profile_page')
                else :
                    user.set_password(new_pass)
                    user.save()
                    messages.success(request, 'Your password reset successfully')
                    login(request, user)
                    return redirect('edit_profile_page')
            else:
                messages.error(request, 'your old password are not match')
                return redirect('edit_profile_page')
        else:
            return HttpResponse('user is not authenticated')
    else:
        return HttpResponse('error 404')


def searcheduser(request,username):
    user = User.objects.get(username = username)
    profile = Profile.objects.get(user = user)
    photos = Photo.objects.none()
    i_follow = Follower_table.objects.none()
    my_followers = Follower_table.objects.none()
    i_follow_user = User.objects.none() # who is followed by  searched user
    my_followers_user = User.objects.none()   # who  follow searched user
    if Photo.objects.filter(upload_by = user).exists():
        photos = Photo.objects.filter(upload_by = user)

    if Follower_table.objects.filter(following = user).exists():
        my_followers = Follower_table.objects.filter(following = user)
        my_followers_user = []                                      # jo tanuj ko follow karte hi
        for i in my_followers:
            my_followers_user.append(i.follower)

    if Follower_table.objects.filter(follower = user).exists():
        i_follow = Follower_table.objects.filter(follower = user)   # jinko tanuj follow karta hi
        i_follow_user = []
        for j in i_follow:
            i_follow_user.append(j.following)
    
    if request.user in my_followers_user:
        flag = "True"
    else: 
        flag = "False"

    d = {'user':user,'profile':profile,'photos':photos,'i_follow':i_follow,'my_followers':my_followers,'flag':flag}
    return render(request,'persons/searched_user.html',d)


def follow(request,follow_username):
    followed_user = User.objects.get(username = follow_username) # jise follow  karna hi
    f = Follower_table()
    f.follower = request.user
    f.following = followed_user
    f.save()
    next = request.GET['next']
    return redirect(next)


def unfollow(request,unfollow_username):
    unfollow_user = User.objects.get(username = unfollow_username)
    relation = Follower_table.objects.get(follower = request.user,following = unfollow_user)
    relation.delete()
    next = request.GET['next']
    return redirect(next)


def profile_image(request):
    if request.method == 'POST':
        imageuploadform = ImageuploadForm(request.POST, request.FILES)
        if imageuploadform.is_valid():
            image = imageuploadform.cleaned_data.get('image')
            profile = Profile.objects.get(user = request.user)
            profile.profile_picture = image
            profile.save()
            return redirect(request.POST['next'])
        else:
            messages.error(request,'an error occure')
        return redirect(request.POST['next'])    
    else:
        return HttpResponse('request error')