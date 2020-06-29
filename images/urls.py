from django.urls import path 
from . import  views

urlpatterns = [
    path('', views.images, name = 'images'),
    path('upload_image',views.upload_image,name='upload_image'),
    path('like/<int:photo_sno>',views.like, name = 'like'),
    path('dislike/<int:photo_sno>',views.dislike, name = 'dislike'),
    path('comment/<int:photo_sno>',views.comment, name='comment'),
    path('image_detail/<int:photo_sno>',views.detail,name='detail'),
]