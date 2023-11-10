
from django.contrib import admin
from django.urls import include, path
from rest_framework import urls
from django.conf import settings
from django.conf.urls import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('djoser.urls')),
    path('auth/', include('user.urls')),
    path('api/', include('api.urls')),
    path('events/', include('events.urls')),
] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
