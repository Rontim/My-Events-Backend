from django.urls import path, register_converter
from .views import *
from .converters import SlugPrimaryKeyConverter

register_converter(SlugPrimaryKeyConverter, 'slug')

urlpatterns = [
    path('', EventListAPIView.as_view()),
    path('create/', EventCreateAPIView.as_view(), name='event_create'),
    path('<str:slug>/', EventDetailView.as_view(), name='event_detail'),
    path('<str:slug>/update/',
         EventUpdateAPIView.as_view(), name='event-update'),
    path('<str:slug>/delete/',
         EventDeleteAPIView.as_view(), name='event-delete'),
    path('<str:slug>/rsvp/', RSVPView.as_view(), name='event-rsvp'),
    path('user/events/', UserEventsAPIView.as_view(), name='user-events'),
    path('<str:slug>/manage-rsvp/',
         ManageRSVPAPIView.as_view(), name='manage-rsvp'),
    path('<str:slug>/invite/<str:username>/',
         SendInvitationAPIView.as_view(), name='send-invite'),
    path('organizer/dashboard/', OrganizerDashboardAPIView.as_view(),
         name='organizer-dashboard'),
]
