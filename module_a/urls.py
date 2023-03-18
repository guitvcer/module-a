from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from games.views import ServeGameView

urlpatterns = [
    path(f'api/v{settings.VERSION}/auth/', include('authorization.urls')),
    path(f'api/v{settings.VERSION}/games/', include('games.urls')),
    path(f'api/v{settings.VERSION}/users/', include('users.urls')),
    path('games/<slug:slug>/<int:version>', ServeGameView.as_view(), name='serve'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'module_a.views.handler404'
