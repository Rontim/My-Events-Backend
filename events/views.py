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
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organizer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
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
