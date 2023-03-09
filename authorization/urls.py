from django.urls import path
from rest_framework_simplejwt.views import token_refresh

from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view()),
    path('signin/', views.SignInView.as_view()),
    path('signout/', views.SignOutView.as_view()),
    path('refresh/', token_refresh),
]
