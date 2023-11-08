"""
URLs for the API app.
"""

from django.urls import path, include

urlpatterns = [
    path('events/', include('api.events.urls')),
]