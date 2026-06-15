from django.urls import path
from .views import RegisterView,LoginView,ProfileView,CreateOfficerView


urlpatterns=[
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('create-officer/',CreateOfficerView.as_view(),name='create-officer'),
    
]