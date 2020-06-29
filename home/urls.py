from django.urls import path 
from . import  views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('signin_page',views.signin_page ,name = 'signin_page'),
    path('signup_page',views.signup_page ,name = 'signup_page'),
    path('signin', views.signin, name= 'signin'),
    path('signout',views.signout,name = 'signout'),
    path('signup', views.signup, name = 'signup'),
    path('search',views.search, name = 'search')
]
