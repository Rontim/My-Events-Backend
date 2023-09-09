
from django.contrib import admin
from django.urls import include, path
from rest_framework import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/', include('user.urls')),
    path('events/', include('events.urls')),
]
