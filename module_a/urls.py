from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(f'api/v{settings.VERSION}/auth/', include('authorization.urls')),
    path('admin/', admin.site.urls),
]
