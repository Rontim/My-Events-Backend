from math import floor

from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from events.models import Event, RSVP
from events.serializers import EventsDateSerializer, EventSerializer, DashBoardSerializer
from rest_framework import status, permissions
from datetime import date

User = get_user_model()


class EventDates(APIView):
    """
    This view returns a list of all the events' dates in the database.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        events = Event.objects.filter(date__gte=date.today()).order_by('date')
        events_date = EventsDateSerializer(events, many=True).data

        return Response(events_date, status=status.HTTP_200_OK)


class MyEvents(APIView):
    """
    This view returns a list of all the events created by the user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        events = Event.objects.filter(organizer=user).all().order_by('date')
        serialized_events = EventSerializer(events, many=True).data

        return Response(serialized_events, status=status.HTTP_200_OK)


class MyEventStats(APIView):
    """
    This view will return the total number of events created by the user,
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        events_count = Event.objects.filter(organizer=user).all().count()

        events = Event.objects.filter(organizer=user).all().order_by('date')
        serializer = EventSerializer(events, many=True).data

        total_attendees = 0
        revenue = 0.00
        for event in events:
            total_attendees += event.attendees.count()
            revenue += event.total_revenue

        average_attendance = total_attendees / events.count()

        data = {
            'Total Events': events_count,
            'Total Attendees': total_attendees,
            'Total Revenue': revenue,
            'Average Attendance': floor(average_attendance)
        }

        return Response(data)


class RSVPEvent(APIView):
    """
    This view will allow users to RSVP to an event.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, slug):
        event = get_object_or_404(Event, slug=slug)
        user = request.user

        if RSVP.objects.filter(event=event, user=user).exists():
            return Response({"detail": "You've already RSVPed to this event."}, status=status.HTTP_400_BAD_REQUEST)

        rsvp = RSVP(user=user, event=event, is_attending=True)
        rsvp.save()
        return Response({"detail": "RSVP successful."}, status=status.HTTP_201_CREATED)


class MyRSVPs(APIView):
    """
    This view will return a list of all the events the user has RSVPed to.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        registered_events = Event.objects.filter(rsvps__user=user)
        serializer = EventSerializer(registered_events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManageRSVP(APIView):
    """
    This view will allow users to manage their RSVP status.
    """
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, slug):
        event = get_object_or_404(Event, slug=slug)
        user = request.user

        try:
            rsvp = RSVP.objects.get(event=event, user=user)
        except RSVP.DoesNotExist:
            return Response({"detail": "You haven't RSVPed to this event."}, status=status.HTTP_400_BAD_REQUEST)

        rsvp.is_attending = not rsvp.is_attending
        rsvp.save()

        return Response({"detail": "RSVP status updated."}, status=status.HTTP_200_OK)


class SendInvitation(APIView):
    """
    This view will allow users to send invitations to other users.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, slug, username):
        event = get_object_or_404(Event, slug=slug)

        if event.organizer != request.user:
            return Response({"detail": "You don't have permission to send invitations for this event."},
                            status=status.HTTP_403_FORBIDDEN)

        invited_user = get_object_or_404(User, username=username)

        if event.invited_users.filter(username=invited_user.username).exists():
            return Response({"detail": "Invitation already sent to this user."}, status=status.HTTP_400_BAD_REQUEST)

        event.invited_users.add(invited_user)

        return Response({"detail": "Invitation sent."}, status=status.HTTP_201_CREATED)


class OrganizerDashboard(APIView):
    """
    This view will return statistics about the events created by the user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        organizer = request.user
        events = Event.objects.filter(organizer=organizer).all()
        serializer = DashBoardSerializer(events, many=True).data

        return Response(serializer, status=status.HTTP_200_OK)


class EventRegistration(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, slug, fomart=None):
        username = request.data.get('username')

        event = get_object_or_404(Event, slug=slug)

        registered_users = event.registered_users.all()

        user = get_object_or_404(User, username=username)

        if user in registered_users:
            return Response({'detail': 'You\'ve already registered for this event'})

        event.registered_users.add(user)

        return Response({'success': 'You\'ve successfully registered for this event'})
