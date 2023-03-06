from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

from .views import GameViewSet, UploadGameView

app_name = 'games'

router = DefaultRouter()
router.register('', GameViewSet, basename='game')

urlpatterns = [
    *router.urls,
    path('<slug:slug>/upload/', csrf_exempt(UploadGameView.as_view()), name='upload'),
]
