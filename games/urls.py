from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import GameViewSet, ScoreView, UploadGameView

app_name = 'games'

router = DefaultRouter()
router.register('', GameViewSet, basename='game')

urlpatterns = [
    *router.urls,
    path('<slug:slug>/upload/', UploadGameView.as_view(), name='upload'),
    path('<slug:slug>/scores/', ScoreView.as_view(), name='score'),
]
