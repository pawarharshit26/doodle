from django.urls import path 
from . import  views

urlpatterns = [
    path('pro', views.persons_pro, name = 'persons'),
    path('edit_profile_page',views.edit_profile_page, name = 'edit_profile_page'),
    path('edit_profile',views.edit_profile,name = 'edit_profile'),
    path('change_password',views.change_password, name = 'change_password'),
    path('profile_image',views.profile_image, name='profile image'),
    path('unfollow/<str:unfollow_username>',views.unfollow, name = 'unfollow'),
    path('follow/<str:follow_username>',views.follow, name = 'follow'),
    path('<str:username>', views.searcheduser, name = 'searcheduser'),
    
]
