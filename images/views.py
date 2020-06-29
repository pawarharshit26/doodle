from django.shortcuts import render,HttpResponse,redirect
from .models import Photo,Likes,Comment
from .forms import ImageuploadForm
from django.contrib import messages


# Create your views here.
def images(request):
    all_img =  Photo.objects.all()
    all = {'all_img':all_img}
    return render(request,'images/imghome.html',all)
    return HttpResponse('images')

def like(request,photo_sno):
    if request.method == "POST":
        photo = Photo.objects.get(sno = photo_sno) 
        like = Likes()
        like.user = request.user
        like.photo = photo
        like.save()
        return redirect(request.POST['next'])
    else:
        return HttpResponse('request error')

def dislike(request,photo_sno):
    photo = Photo.objects.get(sno = photo_sno)
    like = Likes.objects.get(photo = photo,user = request.user)
    like.delete()
    return redirect(request.POST['next'])

def comment(request,photo_sno):
    if(request.method == 'POST'):
        photo = Photo.objects.get(sno = photo_sno)
        comment = Comment()
        comment.user = request.user
        comment.photo = photo
        comment.text = request.POST['text']
        comment.save()
        return redirect(request.POST['next'])
    else:
        return HttpResponse('request error')


def detail(request,photo_sno):
    photo = Photo.objects.get(sno = photo_sno);
    all_comments = Comment.objects.none()
    if Comment.objects.filter(photo = photo).exists():
        all_comments = Comment.objects.filter(photo = photo)
        all_comments = all_comments.order_by('timestamp').reverse()
    flag = "False"
    like_count = 0
    if Likes.objects.filter(photo = photo).exists:
        all_likes  = Likes.objects.filter(photo = photo)
        for l in all_likes:
            if l.user == request.user:
                flag = "True"
                break
        like_count = len(all_likes)
    d = {'photo':photo,'all_comments':all_comments,'flag':flag,'like_count':like_count}
    return render(request,'images/image_detail.html',d)


def upload_image(request):
    if request.method == 'POST':
        imageuploadform = ImageuploadForm(request.POST, request.FILES)
        if imageuploadform.is_valid():
            image = imageuploadform.cleaned_data.get('image')
            photo = Photo(upload_by = request.user,photo = image)
            photo.save()
            messages.success(request,'image upload successfully')
        else:
            messages.error(request,'an error occure')
        return redirect(request.POST['next'])    
    else:
        return HttpResponse('request error')