from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import GameViewSet, SourceGameView

app_name = 'games'

router = DefaultRouter()
router.register('', GameViewSet, basename='game')

urlpatterns = [
    *router.urls,
    path('<slug:slug>/<int:version>/', SourceGameView.as_view(), name='source'),
]
