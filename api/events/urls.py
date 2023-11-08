"""
This file contains the urls for the events app api operations only.
"""

from django.urls import path
from .view import *

urlpatterns = [
    path('dates/', EventDates.as_view()),
    path('my-events/', MyEvents.as_view()),
    path('my-events/stats/', MyEventStats.as_view()),
    path('rsvp/<str:slug>/', RSVPEvent.as_view()),
    path('rsvp/manage/<str:slug>/', ManageRSVP.as_view()),
    path('my-rsvps/', MyRSVPs.as_view()),
    path('<str:slug>/invite/<str:username>/', SendInvitation.as_view()),
    path('organizer/dashboard/', OrganizerDashboard.as_view()),
    path('register/<str:slug>/', EventRegistration.as_view()),
]
