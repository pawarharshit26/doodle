from django.shortcuts import render,redirect
from django.http import HttpResponse

from django.contrib.auth.models import User
from persons.models import Profile,Follower_table
from images.models import Photo,Likes

from django.contrib.auth import authenticate, login ,logout
from django.contrib import messages

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        propic = Profile.objects.get(user = request.user).profile_picture
        
        cur_user = request.user
        cur_user_followings = Follower_table.objects.filter(follower = cur_user)
        all_photos = Photo.objects.none()
        for i in cur_user_followings:
            if Photo.objects.filter(upload_by = i.following).exists():
                ith_following_photos = Photo.objects.filter(upload_by = i.following)
                all_photos = all_photos.union(ith_following_photos)

        if Photo.objects.filter(upload_by =  cur_user).exists():
            cur_user_photos = Photo.objects.filter(upload_by =  cur_user)
            all_photos = all_photos.union(cur_user_photos)

        all_photos = all_photos.order_by('upload_time').reverse()
        res = []
        for i in all_photos:
            if Likes.objects.filter(photo = i).exists():
                likes_on_i = Likes.objects.filter(photo = i)
                for l in likes_on_i:
                    if(l.user == request.user):
                        res.append((i,"True",len(likes_on_i)))
                        break
                else:
                    res.append((i,"False",len(likes_on_i)))
            else:
                res.append((i,"False",0))

        d = {'propic':propic,'all_photos':all_photos,'res':res}
        return render(request,'home/home.html',d)
    else:
        return render(request,'home/home.html')
    # return HttpResponse('Home page')


def signin_page(request):
    return render(request,'home/signin_page.html')

def signup_page(request):
    return render(request,'home/signup_page.html')

def signin(request):
    if(request.method == 'POST'):
        username = request.POST['username']
        if(User.objects.filter(username = username).exists()):
            password = request.POST['password']
            user = authenticate(username= username,password = password)
            if user is not None:
                login(request, user)
                messages.success(request,'Login is Successful')
                return redirect('home')
            else:
                messages.error(request,'Invalid Credentials')
                return redirect('home')
        else:
            messages.error(request,"User is not registered.please signup")
            return redirect('home')
    
    return HttpResponse('error 404')


def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if len(username) > 10:
            messages.error(request, 'Username is very large')
            return redirect('signup_page')
        if User.objects.filter(username=username).exists():
            messages.error(request,"this Username is not available")
            return redirect('signup_page')
        if User.objects.filter(email=email).exists():
            messages.error(request,"this email is already registered")
            return redirect('signup_page')
        if password != cpassword:
            messages.error(request, 'passwords are not match')
            return redirect('signup_page')
        
        myuser = User.objects.create_user(username = username,email = email,password = password)
        myuser.save()
        myuser_profile = Profile(user = myuser)
        myuser_profile.save()
        messages.success(request, 'Your Nature Window account is created')
        return redirect('home')
    else:
        return HttpResponse("404 - Not Found")
    

def signout(request):
    logout(request)
    messages.success(request,'Successfully Logout')
    return redirect('home')


def search(request):
    query = request.GET['search_query']
    if(len(query) >  40):
        searchedusers = User.objects.none()
        searchedprofiles = Profile.objects.none()
        user_profile = [(searchedusers,searchedprofiles)]
        messages.warning(request,'query is too large try small query')
    else:
        usernames = User.objects.filter(username__icontains = query)
        firstnames = User.objects.filter(first_name__icontains = query)
        searchedusers = usernames.union(firstnames)
        lastnames = User.objects.filter(last_name__icontains = query)
        searchedusers = list(searchedusers.union(lastnames))
        if request.user in  searchedusers:
            searchedusers.remove(request.user)
        profiles = []
        user_profile = []
        for users in searchedusers:
            profile = Profile.objects.get(user = users)
            user_profile.append((users,profile))
        print(user_profile)
    if len(searchedusers) == 0:
        messages.warning(request,'No search result found refine your query')

    results = {'user_profile':user_profile,'query':query}
    return render(request,'home/search.html',results)