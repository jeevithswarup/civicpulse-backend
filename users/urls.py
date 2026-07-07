from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, ProfileView, CreateOfficerView


urlpatterns=[
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('create-officer/', CreateOfficerView.as_view(), name='create-officer'),
    # JWT refresh — used by the frontend API client on 401
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]