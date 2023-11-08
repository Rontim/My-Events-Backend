import datetime
from datetime import date
from logging import Logger
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import RSVP, Event
from .serializers import EventSerializer, DashBoardSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class EventCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        event = {}
        images = data.get('images', None)
        if images:
            if len(images) > 1:
                for i in range(len(images)):
                    event[f'event_image{i + 1}'] = images[i]
            else:
                event['event_image1'] = images[0]
        event['title'] = data.get('title', None)
        event['description'] = data.get('description', None)
        event['date'] = data.get('date', None)
        event['time'] = data.get('time', None)
        event['location'] = data.get('location', None)
        event['category'] = data.get('category', None)
        event['max_capacity'] = data.get('max_capacity', None)
        event['ticket_price'] = data.get('ticket_price', None)
        event['organizer'] = request.user.id
        serializer = EventSerializer(data=event)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"detail": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


class EventDetailView(APIView):
    def get(self, request, slug):
        event = get_object_or_404(Event, slug=slug)
        print(event)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        events = Event.objects.filter(date__gte=date.today()).order_by('date')
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, slug):
        event = get_object_or_404(Event, slug=slug)

        if event.organizer != request.user:
            return Response({"detail": "You don't have permission to update this event."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = EventSerializer(event, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, slug):
        event = get_object_or_404(Event, slug=slug)

        if event.organizer != request.user:
            return Response({"detail": "You don't have permission to delete this event."},
                            status=status.HTTP_403_FORBIDDEN)

        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
