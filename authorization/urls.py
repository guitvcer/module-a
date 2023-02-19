from django.urls import path

from . import views

urlpatterns = [
    path('sign_up/', views.SignUpView.as_view()),
    path('sign_in/', views.SignInView.as_view()),
]
