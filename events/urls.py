"""
This file contains the urls for the events app CRUD operations only.
"""

from django.urls import path
from .views import *


urlpatterns = [
    path('', EventListAPIView.as_view()),
    path('create/', EventCreateAPIView.as_view(), name='event_create'),
    path('<str:slug>/', EventDetailView.as_view(), name='event_detail'),
    path('<str:slug>/update/',
         EventUpdateAPIView.as_view(), name='event-update'),
    path('<str:slug>/delete/',
         EventDeleteAPIView.as_view(), name='event-delete'),
]
