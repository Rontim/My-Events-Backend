from math import floor
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from events.models import Event
from events.serializers import EventsDateSerializer, EventSerializer
from logging import Logger
from rest_framework import status
from datetime import date


class EventDates(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        events = Event.objects.filter(date__gte=date.today()).order_by('date')
        events_date = EventsDateSerializer(events, many=True).data

        return Response(events_date, status=status.HTTP_200_OK)


class MyEvents(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        events = Event.objects.filter(organizer=user).all().order_by('date')
        serialized_events = EventSerializer(events, many=True).data

        return Response(serialized_events, status=status.HTTP_200_OK)


class MyEventStats(APIView):
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
