from datetime import date
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import RSVP, Event
from .serializers import EventSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


class EventCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organizer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailView(APIView):
    def get(self, request, slug):
        event = get_object_or_404(Event, slug=slug)
        print(event)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        events = Event.objects.filter(date__gte=date.today())
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, slug):
        event = get_object_or_404(Event, slug=slug)

        if event.organizer != request.user:
            return Response({"detail": "You don't have permission to update this event."}, status=status.HTTP_403_FORBIDDEN)

        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, slug):
        event = get_object_or_404(Event, slug=slug)

        if event.organizer != request.user:
            return Response({"detail": "You don't have permission to delete this event."}, status=status.HTTP_403_FORBIDDEN)

        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RSVPView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, slug):
        event = get_object_or_404(Event, slug=slug)
        user = request.user

        if RSVP.objects.filter(event=event, user=user).exists():
            return Response({"detail": "You've already RSVPed to this event."}, status=status.HTTP_400_BAD_REQUEST)

        rsvp = RSVP(user=user, event=event, is_attending=True)
        rsvp.save()
        return Response({"detail": "RSVP successful."}, status=status.HTTP_201_CREATED)


class UserEventsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        registered_events = Event.objects.filter(rsvps__user=user)
        serializer = EventSerializer(registered_events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ManageRSVPAPIView(APIView):
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


class SendInvitationAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, slug, username):
        event = get_object_or_404(Event, slug=slug)

        if event.organizer != request.user:
            return Response({"detail": "You don't have permission to send invitations for this event."}, status=status.HTTP_403_FORBIDDEN)

        invited_user = get_object_or_404(User, username=username)

        if event.invited_users.filter(id=invited_user.id).exists():
            return Response({"detail": "Invitation already sent to this user."}, status=status.HTTP_400_BAD_REQUEST)

        event.invited_users.add(invited_user)

        return Response({"detail": "Invitation sent."}, status=status.HTTP_201_CREATED)


class OrganizerDashboardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        organizer = request.user
        events_created = Event.objects.filter(organizer=organizer)
        serializer = EventSerializer(events_created, many=True)

        events_attendees = {}

        for event in events_created:
            events_attendees[event.pk] = event.rsvps.filter(
                is_attending=True).count()

        data = {
            "events_created": serializer.data,
            "event_attendees": events_attendees,
        }

        return Response(data, status=status.HTTP_200_OK)
