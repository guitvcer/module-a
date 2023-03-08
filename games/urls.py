from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CreateScoreView, GameViewSet, ServeGameView, UploadGameView

app_name = 'games'

router = DefaultRouter()
router.register('', GameViewSet, basename='game')

urlpatterns = [
    *router.urls,
    path('<slug:slug>/upload/', UploadGameView.as_view(), name='upload'),
    path('<slug:slug>/<int:version>/', ServeGameView.as_view(), name='serve'),
    path('<slug:slug>/scores/', CreateScoreView.as_view(), name='create_score'),
]
