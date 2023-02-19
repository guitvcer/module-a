from django.urls import path

from . import views

urlpatterns = [
    path('', views.CreateGameAPIView.as_view()),
]
