from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view()),
    path('signin/', views.SignInView.as_view()),
]
