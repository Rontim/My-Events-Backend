from django.urls import path
from events.api.api import EventDates, MyEvents, MyEventStats

urlpatterns = [
    path('event/date/', EventDates.as_view(), name='date'),
    path('events/', MyEvents.as_view(), name='my-events'),
    path('events/stats/', MyEventStats.as_view(), name='my-stats')
]
